"""
Script to generate schema.yaml file from a dataset CSV file.
This script analyzes the dataset and automatically creates a schema configuration file.

Usage:
    python scripts/generate_schema.py --data_path <path_to_csv> --output_path config/schema.yaml
    python scripts/generate_schema.py --data_path data/train.csv --output_path config/schema.yaml
"""

import argparse
import os
import sys
import pandas as pd
import numpy as np
import yaml
from pathlib import Path

# Add parent directory to path to import project modules
sys.path.append(str(Path(__file__).parent.parent))

from src.forest.logger import logging
from src.forest.utils.main_utils import write_yaml_file


def detect_column_types(df: pd.DataFrame) -> dict:
    """
    Detect column types (numerical vs categorical) from dataframe
    :param df: DataFrame to analyze
    :return: Dictionary with column type information
    """
    numerical_columns = []
    categorical_columns = []
    columns_info = []
    
    for col in df.columns:
        col_type = str(df[col].dtype)
        
        # Determine if column is numerical or categorical
        if df[col].dtype in ['int64', 'int32', 'float64', 'float32']:
            # Check if it's actually categorical (low cardinality integers)
            unique_count = df[col].nunique()
            total_count = len(df[col])
            
            # If unique values are less than 20% of total and less than 50 unique values, consider categorical
            if unique_count < 50 and unique_count / total_count < 0.2:
                categorical_columns.append(col)
                columns_info.append({col: "category"})
            else:
                numerical_columns.append(col)
                columns_info.append({col: "int" if 'int' in col_type else "float"})
        else:
            categorical_columns.append(col)
            columns_info.append({col: "category"})
    
    return {
        "numerical_columns": numerical_columns,
        "categorical_columns": categorical_columns,
        "columns_info": columns_info
    }


def generate_schema(data_path: str, output_path: str, target_column: str = None, drop_columns: list = None):
    """
    Generate schema.yaml file from dataset
    :param data_path: Path to CSV file
    :param output_path: Path where schema.yaml will be saved
    :param target_column: Name of target column (will be marked as categorical)
    :param drop_columns: List of columns to drop (optional)
    """
    try:
        logging.info(f"Reading dataset from: {data_path}")
        df = pd.read_csv(data_path)
        
        logging.info(f"Dataset shape: {df.shape}")
        logging.info(f"Columns: {list(df.columns)}")
        
        # Automatically treat accidental index columns as drop columns
        detected_unnamed = [c for c in df.columns if str(c).startswith("Unnamed")]
        drop_columns = list(drop_columns) if drop_columns else []
        for c in detected_unnamed:
            if c not in drop_columns:
                drop_columns.append(c)

        drop_set = set(drop_columns or [])

        # Define feature lists. For this dataset, all non-target columns are numeric features.
        numeric_cols = list(df.select_dtypes(include=[np.number]).columns)
        non_numeric_cols = [c for c in df.columns if c not in numeric_cols]

        numerical_columns = [c for c in numeric_cols if c not in drop_set and c != target_column]
        categorical_columns = []
        if target_column and target_column in df.columns and target_column not in drop_set:
            categorical_columns.append(target_column)
        categorical_columns.extend([c for c in non_numeric_cols if c not in drop_set and c not in categorical_columns])

        # Build columns list with types (matching the existing schema.yaml format)
        # Format: [{column_name: type}, ...]
        columns_list = []
        for col in df.columns:
            if col in drop_set:
                continue
            if col == target_column:
                col_type = "category"
            else:
                if pd.api.types.is_float_dtype(df[col].dtype):
                    col_type = "float"
                elif pd.api.types.is_integer_dtype(df[col].dtype):
                    col_type = "int"
                else:
                    col_type = "category"
            
            # Format: {column_name: type} as dictionary
            columns_list.append({col: col_type})
        
        # Build schema dictionary matching the existing format
        schema = {
            "columns": columns_list,
            "numerical_columns": numerical_columns,
            "categorical_columns": categorical_columns,
            "drop_columns": drop_columns if drop_columns else []
        }
        
        # Write schema to file
        logging.info(f"Writing schema to: {output_path}")
        write_yaml_file(file_path=output_path, content=schema)
        
        logging.info("Schema generation completed successfully!")
        logging.info(f"Numerical columns: {len(numerical_columns)}")
        logging.info(f"Categorical columns: {len(categorical_columns)}")
        logging.info(f"Drop columns: {len(schema['drop_columns'])}")
        
        return schema
        
    except Exception as e:
        logging.error(f"Error generating schema: {str(e)}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Generate schema.yaml from dataset")
    parser.add_argument(
        "--data_path",
        type=str,
        required=True,
        help="Path to CSV dataset file"
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default="config/schema.yaml",
        help="Path where schema.yaml will be saved (default: config/schema.yaml)"
    )
    parser.add_argument(
        "--target_column",
        type=str,
        default=None,
        help="Name of target column (default: None)"
    )
    parser.add_argument(
        "--drop_columns",
        type=str,
        nargs="+",
        default=None,
        help="List of columns to drop (space-separated)"
    )
    
    args = parser.parse_args()
    
    # Check if data file exists
    if not os.path.exists(args.data_path):
        print(f"Error: Data file not found at {args.data_path}")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(args.output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # Generate schema
    try:
        schema = generate_schema(
            data_path=args.data_path,
            output_path=args.output_path,
            target_column=args.target_column,
            drop_columns=args.drop_columns
        )
        print(f"\nOK: Schema successfully generated at: {args.output_path}")
        print(f"\nSchema Summary:")
        print(f"  - Total columns: {len(schema['columns'])}")
        print(f"  - Numerical columns: {len(schema['numerical_columns'])}")
        print(f"  - Categorical columns: {len(schema['categorical_columns'])}")
        print(f"  - Drop columns: {len(schema['drop_columns'])}")
        if schema['drop_columns']:
            print(f"  - Columns to drop: {', '.join(schema['drop_columns'])}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
