import sys
import os
import pandas as pd
import numpy as np
from pandas import DataFrame
from src.forest.exception import ForestException
from src.forest.logger import logging
from src.forest.utils.main_utils import read_yaml_file, write_yaml_file
from src.forest.constant.training_pipeline import SCHEMA_FILE_PATH
from src.forest.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.forest.entity.config_entity import DataValidationConfig

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_config = data_validation_config
        self._schema_config =read_yaml_file(file_path=SCHEMA_FILE_PATH)
    
    def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
        """

        :param dataframe:
        :return: True if required columns present
        """
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])
            logging.info(f"Is required column present: [{status}]")
            return status
        except Exception as e:
            raise ForestException(e, sys)
    
    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise ForestException(e, sys)
    
    def is_numerical_column_exist(self, df: DataFrame) -> bool:
        """
        This function check numerical column is present in dataframe or not
        :param df:
        :return: True if all column presents else False
        """
        try:
            dataframe_columns = df.columns
            status = True
            missing_numerical_columns = []
            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    status = False
                    missing_numerical_columns.append(column)
            logging.info(f"Missing numerical column: {missing_numerical_columns}")
            return status
        except Exception as e:
            raise ForestException(e, sys) from e
    
    def detect_outliers(self, df: DataFrame) -> dict:
        """
        Detect outliers in numerical columns using IQR (Interquartile Range) method
        :param df: DataFrame to check for outliers
        :return: Dictionary with outlier information for each column
        """
        try:
            outlier_report = {}
            numerical_columns = [col for col in self._schema_config["numerical_columns"] if col in df.columns]
            
            for column in numerical_columns:
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
                outlier_count = len(outliers)
                outlier_percentage = (outlier_count / len(df)) * 100
                
                outlier_report[column] = {
                    "lower_bound": float(lower_bound),
                    "upper_bound": float(upper_bound),
                    "outlier_count": int(outlier_count),
                    "outlier_percentage": float(outlier_percentage),
                    "Q1": float(Q1),
                    "Q3": float(Q3),
                    "IQR": float(IQR)
                }
                
                logging.info(f"Column {column}: {outlier_count} outliers ({outlier_percentage:.2f}%)")
            
            return outlier_report
        except Exception as e:
            raise ForestException(e, sys) from e

    def initiate_data_validation(self) -> bool:
        """
        Method Name :   initiate_data_validation
        Description :   This method initiates the data validation component for the pipeline
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered initiate_data_validation method of Data_Validation class")
        try:

            validation_error_msg = ""
            logging.info("Starting data validation")
            train_df, test_df = (DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path),
                                 DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path))

            status = self.validate_number_of_columns(dataframe=train_df)
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe."
            
            status = self.validate_number_of_columns(dataframe=test_df)

            logging.info(f"All required columns present in testing dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in test dataframe."

            status = self.is_numerical_column_exist(df=train_df)

            if not status:
                validation_error_msg += f"Numerical columns are missing in training dataframe."

            status = self.is_numerical_column_exist(df=test_df)

            if not status:
                validation_error_msg += f"Numerical columns are missing in test dataframe."
            
            validation_status = len(validation_error_msg) == 0
            
            # Perform outlier detection
            logging.info("Starting outlier detection on training data")
            train_outlier_report = self.detect_outliers(train_df)
            logging.info("Starting outlier detection on testing data")
            test_outlier_report = self.detect_outliers(test_df)
            
            # Save outlier reports
            outlier_report_path = os.path.join(
                os.path.dirname(self.data_validation_config.drift_report_file_path),
                "outlier_report.yaml"
            )
            outlier_report = {
                "train_outliers": train_outlier_report,
                "test_outliers": test_outlier_report
            }
            write_yaml_file(file_path=outlier_report_path, content=outlier_report)
            logging.info(f"Outlier report saved to: {outlier_report_path}")
            
            if validation_status:
                # drift_status = self.detect_dataset_drift(train_df, test_df)
                # if drift_status:
                #     logging.info(f"Drift detected.")
                data_validation_artifact = DataValidationArtifact(
                    validation_status=validation_status,
                    valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                    valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                    invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                    invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                    drift_report_file_path=self.data_validation_config.drift_report_file_path
                )
                logging.info(f"Data validation artifact: {data_validation_artifact}")
                return data_validation_artifact
            else:
                logging.info(f"Validation_error: {validation_error_msg}")
                data_validation_artifact = DataValidationArtifact(
                    validation_status=validation_status,
                    valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                    valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                    invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                    invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                    drift_report_file_path=self.data_validation_config.drift_report_file_path
                )
                logging.info(f"Data validation artifact: {data_validation_artifact}")
                return data_validation_artifact

        except Exception as e:
            raise ForestException(e, sys) from e
