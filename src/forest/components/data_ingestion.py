import sys
import os
import shutil
import pandas as pd
from pandas import DataFrame
from zipfile import ZipFile
from sklearn.model_selection import train_test_split
from src.forest.entity.config_entity import DataIngestionConfig
from src.forest.entity.artifact_entity import DataIngestionArtifact
from src.forest.exception import ForestException
from src.forest.logger import logging
from src.forest.utils.main_utils import read_yaml_file, create_directories
from src.forest.constant.training_pipeline import SCHEMA_FILE_PATH

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise ForestException(e,sys)
    
    def export_data_into_feature_store(self)->DataFrame:
        try:
            logging.info(f"Extracting data from local zip file: {self.data_ingestion_config.zip_file_path}")
            
            # Check if zip file exists
            if not os.path.exists(self.data_ingestion_config.zip_file_path):
                raise FileNotFoundError(f"Zip file not found at: {self.data_ingestion_config.zip_file_path}")
            
            # Extract zip file
            extract_dir = os.path.join(os.path.dirname(self.data_ingestion_config.zip_file_path), "extracted")
            os.makedirs(extract_dir, exist_ok=True)
            
            with ZipFile(self.data_ingestion_config.zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
                logging.info(f"Extracted zip file to: {extract_dir}")
            
            # Find CSV file in extracted directory
            csv_files = [f for f in os.listdir(extract_dir) if f.endswith('.csv')]
            if not csv_files:
                raise FileNotFoundError(f"No CSV file found in extracted directory: {extract_dir}")
            
            # Read the first CSV file found (assuming train.csv or similar)
            csv_file_path = os.path.join(extract_dir, csv_files[0])
            logging.info(f"Reading CSV file: {csv_file_path}")
            dataframe = pd.read_csv(csv_file_path)

            # Drop accidental index columns like "Unnamed: 0"
            unnamed_cols = [c for c in dataframe.columns if str(c).startswith("Unnamed")]
            if unnamed_cols:
                logging.info(f"Dropping unnamed columns: {unnamed_cols}")
                dataframe = dataframe.drop(columns=unnamed_cols, errors="ignore")
            
            logging.info(f"Shape of dataframe: {dataframe.shape}")
            feature_store_file_path  = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"Saving extracted data into feature store file path: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            
            # Clean up extracted directory after saving
            shutil.rmtree(extract_dir)
            logging.info(f"Cleaned up extracted directory: {extract_dir}")
            
            return dataframe

        except Exception as e:
            raise ForestException(e,sys)

    def split_data_as_train_test(self,dataframe: DataFrame) ->None:
        """
        Method Name :   split_data_as_train_test
        Description :   This method splits the dataframe into train set and test set based on split ratio 
        
        Output      :   Folder is created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered split_data_as_train_test method of Data_Ingestion class")

        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on the dataframe")
            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            logging.info(f"Exporting train and test file path.")
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)

            logging.info(f"Exported train and test file path.")
        except Exception as e:
            raise ForestException(e, sys) from e


    def initiate_data_ingestion(self) ->DataIngestionArtifact:
        """
        Method Name :   initiate_data_ingestion
        Description :   This method initiates the data ingestion components of training pipeline 
        
        Output      :   train set and test set are returned as the artifacts of data ingestion components
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")

        try:
            dataframe = self.export_data_into_feature_store()
            _schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)

            dataframe = dataframe.drop(_schema_config.get("drop_columns", []), axis=1, errors="ignore")

            logging.info("Got the data from zip file and dropped specified columns")

            self.split_data_as_train_test(dataframe)

            logging.info("Performed train test split on the dataset")

            logging.info(
                "Exited initiate_data_ingestion method of Data_Ingestion class"
            )

            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                            test_file_path=self.data_ingestion_config.testing_file_path)
            
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise ForestException(e, sys) from e
