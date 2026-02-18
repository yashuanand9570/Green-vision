"""
MongoDB Operations Utility Module

This module provides convenient wrapper functions for MongoDB operations,
making it easier to interact with MongoDB for data storage and retrieval.
"""

import sys
from typing import Optional, List, Dict, Any
import pandas as pd
from src.forest.logger import logging
from src.forest.exception import ForestException
from src.forest.configuration.mongo_db_connection import MongoDBClient


class MongoDBOperations:
    """Convenience wrapper for MongoDB operations"""
    
    def __init__(self, database_name: Optional[str] = None):
        """
        Initialize MongoDB operations
        
        Args:
            database_name: Optional database name (uses default if not provided)
        """
        try:
            self.client = MongoDBClient(database_name=database_name) if database_name else MongoDBClient()
            self.database = self.client.database
            logging.info(f"MongoDBOperations initialized for database: {self.client.database_name}")
        except Exception as e:
            raise ForestException(e, sys) from e
    
    def insert_data(self, collection_name: str, data: List[Dict[str, Any]]) -> bool:
        """
        Insert data into a collection
        
        Args:
            collection_name: Name of the collection
            data: List of documents to insert
            
        Returns:
            bool: True if successful
        """
        try:
            collection = self.database[collection_name]
            
            if isinstance(data, list):
                collection.insert_many(data)
            else:
                collection.insert_one(data)
            
            logging.info(f"Inserted {len(data) if isinstance(data, list) else 1} documents into {collection_name}")
            return True
        except Exception as e:
            logging.error(f"Error inserting data: {str(e)}")
            raise ForestException(e, sys) from e
    
    def find_data(self, collection_name: str, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Find data in a collection
        
        Args:
            collection_name: Name of the collection
            query: Optional query filter (finds all if None)
            
        Returns:
            List of documents
        """
        try:
            collection = self.database[collection_name]
            query = query or {}
            
            results = list(collection.find(query))
            logging.info(f"Found {len(results)} documents in {collection_name}")
            return results
        except Exception as e:
            logging.error(f"Error finding data: {str(e)}")
            raise ForestException(e, sys) from e
    
    def get_dataframe(self, collection_name: str, query: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Get data as pandas DataFrame
        
        Args:
            collection_name: Name of the collection
            query: Optional query filter
            
        Returns:
            pd.DataFrame: Data as DataFrame
        """
        try:
            data = self.find_data(collection_name, query)
            
            if data:
                df = pd.DataFrame(data)
                # Remove MongoDB _id field if present
                if '_id' in df.columns:
                    df = df.drop('_id', axis=1)
                logging.info(f"Created DataFrame with shape {df.shape}")
                return df
            else:
                logging.warning(f"No data found in {collection_name}")
                return pd.DataFrame()
        except Exception as e:
            logging.error(f"Error creating DataFrame: {str(e)}")
            raise ForestException(e, sys) from e
    
    def insert_dataframe(self, collection_name: str, df: pd.DataFrame) -> bool:
        """
        Insert pandas DataFrame into collection
        
        Args:
            collection_name: Name of the collection
            df: DataFrame to insert
            
        Returns:
            bool: True if successful
        """
        try:
            records = df.to_dict('records')
            self.insert_data(collection_name, records)
            logging.info(f"Inserted DataFrame with {len(records)} rows into {collection_name}")
            return True
        except Exception as e:
            logging.error(f"Error inserting DataFrame: {str(e)}")
            raise ForestException(e, sys) from e
    
    def update_data(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        """
        Update data in a collection
        
        Args:
            collection_name: Name of the collection
            query: Query to match documents
            update: Update operations
            
        Returns:
            int: Number of documents updated
        """
        try:
            collection = self.database[collection_name]
            result = collection.update_many(query, {'$set': update})
            
            logging.info(f"Updated {result.modified_count} documents in {collection_name}")
            return result.modified_count
        except Exception as e:
            logging.error(f"Error updating data: {str(e)}")
            raise ForestException(e, sys) from e
    
    def delete_data(self, collection_name: str, query: Dict[str, Any]) -> int:
        """
        Delete data from a collection
        
        Args:
            collection_name: Name of the collection
            query: Query to match documents to delete
            
        Returns:
            int: Number of documents deleted
        """
        try:
            collection = self.database[collection_name]
            result = collection.delete_many(query)
            
            logging.info(f"Deleted {result.deleted_count} documents from {collection_name}")
            return result.deleted_count
        except Exception as e:
            logging.error(f"Error deleting data: {str(e)}")
            raise ForestException(e, sys) from e
    
    def collection_exists(self, collection_name: str) -> bool:
        """
        Check if a collection exists
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            bool: True if collection exists
        """
        try:
            collections = self.database.list_collection_names()
            exists = collection_name in collections
            logging.info(f"Collection {collection_name} exists: {exists}")
            return exists
        except Exception as e:
            logging.error(f"Error checking collection existence: {str(e)}")
            raise ForestException(e, sys) from e
