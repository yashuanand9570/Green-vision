import logging
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
import pickle
import os

logger = logging.getLogger(__name__)

class TrainPipeline:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        
    def run_pipeline(self):
        """Execute the training pipeline"""
        try:
            logger.info("Starting training pipeline...")
            
            # Load data
            data = self.load_data()
            
            # Preprocess data
            X, y = self.preprocess_data(data)
            
            # Train model
            self.train_model(X, y)
            
            # Save model
            self.save_model()
            
            logger.info("Training pipeline completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error in training pipeline: {str(e)}")
            raise
    
    def load_data(self):
        """Load training data"""
        try:
            data = pd.read_csv('data/training_data.csv')
            logger.info(f"Data loaded with shape: {data.shape}")
            return data
        except FileNotFoundError:
            # Create sample data if not found
            logger.warning("Training data not found. Using sample data.")
            return pd.DataFrame()
    
    def preprocess_data(self, data):
        """Preprocess data for training"""
        if data.empty:
            logger.warning("Empty dataset provided")
            return None, None
        
        # Separate features and target
        X = data.iloc[:, :-1]
        y = data.iloc[:, -1]
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        logger.info(f"Data preprocessed. Features shape: {X_scaled.shape}")
        return X_scaled, y
    
    def train_model(self, X, y):
        """Train the machine learning model"""
        if X is None or y is None:
            logger.warning("No data to train model")
            return
        
        try:
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.model.fit(X, y)
            logger.info("Model trained successfully!")
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            raise
    
    def save_model(self):
        """Save trained model and scaler"""
        try:
            os.makedirs('models', exist_ok=True)
            
            with open('models/model.pkl', 'wb') as f:
                pickle.dump(self.model, f)
            
            with open('models/scaler.pkl', 'wb') as f:
                pickle.dump(self.scaler, f)
            
            logger.info("Model and scaler saved successfully!")
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            raise
