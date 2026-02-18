"""
S3 Operations Utility Module

This module provides convenient wrapper functions for AWS S3 operations,
making it easier to interact with S3 buckets for model storage and predictions.
"""

import os
import sys
from typing import Optional
from src.forest.logger import logging
from src.forest.exception import ForestException
from src.forest.cloud_storage.aws_storage import SimpleStorageService


class S3Operations:
    """Convenience wrapper for S3 operations"""
    
    def __init__(self):
        """Initialize S3 operations"""
        try:
            self.s3 = SimpleStorageService()
            logging.info("S3Operations initialized successfully")
        except Exception as e:
            raise ForestException(e, sys) from e
    
    def upload_model(self, local_path: str, bucket_name: str, s3_key: str) -> bool:
        """
        Upload a model file to S3
        
        Args:
            local_path: Path to local model file
            bucket_name: Name of S3 bucket
            s3_key: Key/path in S3 bucket
            
        Returns:
            bool: True if successful
        """
        try:
            logging.info(f"Uploading model from {local_path} to s3://{bucket_name}/{s3_key}")
            self.s3.upload_file(
                from_filename=local_path,
                to_filename=s3_key,
                bucket_name=bucket_name
            )
            logging.info("Model uploaded successfully")
            return True
        except Exception as e:
            logging.error(f"Error uploading model: {str(e)}")
            raise ForestException(e, sys) from e
    
    def download_model(self, bucket_name: str, s3_key: str, local_path: str) -> bool:
        """
        Download a model file from S3
        
        Args:
            bucket_name: Name of S3 bucket
            s3_key: Key/path in S3 bucket
            local_path: Path to save model locally
            
        Returns:
            bool: True if successful
        """
        try:
            logging.info(f"Downloading model from s3://{bucket_name}/{s3_key}")
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Get file object and read content
            file_obj = self.s3.get_file_object(s3_key, bucket_name)
            content = self.s3.read_object(file_obj, decode=False)
            
            # Write to local file
            with open(local_path, 'wb') as f:
                f.write(content)
            
            logging.info(f"Model downloaded to {local_path}")
            return True
        except Exception as e:
            logging.error(f"Error downloading model: {str(e)}")
            raise ForestException(e, sys) from e
    
    def upload_predictions(self, local_path: str, bucket_name: str, s3_key: Optional[str] = None) -> str:
        """
        Upload predictions CSV to S3
        
        Args:
            local_path: Path to local predictions file
            bucket_name: Name of S3 bucket
            s3_key: Optional key/path in S3 bucket (defaults to filename)
            
        Returns:
            str: S3 key where file was uploaded
        """
        try:
            if s3_key is None:
                s3_key = os.path.basename(local_path)
            
            logging.info(f"Uploading predictions from {local_path} to s3://{bucket_name}/{s3_key}")
            self.s3.upload_file(
                from_filename=local_path,
                to_filename=s3_key,
                bucket_name=bucket_name,
                remove=False  # Keep local copy
            )
            logging.info("Predictions uploaded successfully")
            return s3_key
        except Exception as e:
            logging.error(f"Error uploading predictions: {str(e)}")
            raise ForestException(e, sys) from e
    
    def check_file_exists(self, bucket_name: str, s3_key: str) -> bool:
        """
        Check if a file exists in S3
        
        Args:
            bucket_name: Name of S3 bucket
            s3_key: Key/path in S3 bucket
            
        Returns:
            bool: True if file exists
        """
        try:
            exists = self.s3.s3_key_path_available(bucket_name, s3_key)
            logging.info(f"File s3://{bucket_name}/{s3_key} exists: {exists}")
            return exists
        except Exception as e:
            logging.error(f"Error checking file existence: {str(e)}")
            raise ForestException(e, sys) from e
