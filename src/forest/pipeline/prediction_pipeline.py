import logging
import pandas as pd
import pickle
import os
import boto3
from datetime import datetime

logger = logging.getLogger(__name__)

class PredictionPipeline:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.s3_client = None
        self.load_model()
        
    def load_model(self):
        """Load saved model and scaler"""
        try:
            if os.path.exists('models/model.pkl'):
                with open('models/model.pkl', 'rb') as f:
                    self.model = pickle.load(f)
                
                with open('models/scaler.pkl', 'rb') as f:
                    self.scaler = pickle.load(f)
                
                logger.info("Model and scaler loaded successfully!")
            else:
                logger.warning("Model files not found. Using dummy model.")
                self.model = None
                self.scaler = None
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
def initiate_prediction(self):
        """Initiate prediction pipeline"""
        try:
            logger.info("Starting prediction pipeline...")
            
            # Load prediction data
            data = self.load_prediction_data()
            
            if data is None or data.empty:
                logger.warning("No prediction data found")
                return
            
            # Make predictions
            predictions = self.make_predictions(data)
            
            # Save predictions
            self.save_predictions(predictions)
            
            logger.info("Prediction pipeline completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error in prediction pipeline: {str(e)}")
            raise
    
    def load_prediction_data(self):
        """Load data for prediction"""
        try:
            if os.path.exists('data/prediction_data.csv'):
                data = pd.read_csv('data/prediction_data.csv')
                logger.info(f"Prediction data loaded with shape: {data.shape}")
                return data
            else:
                logger.warning("Prediction data file not found")
                return None
        except Exception as e:
            logger.error(f"Error loading prediction data: {str(e)}")
            return None
    
    def make_predictions(self, data):
        """Make predictions on the data"""
        try:
            if self.model is None:
                logger.warning("Model not available. Using random predictions.")
                predictions = [0] * len(data)
            else:
                # Scale data
                X_scaled = self.scaler.transform(data)
                # Make predictions
                predictions = self.model.predict(X_scaled)
            
            logger.info(f"Predictions made for {len(predictions)} samples")
            return predictions
        except Exception as e:
            logger.error(f"Error making predictions: {str(e)}")
            raise
    
    def save_predictions(self, predictions):
        """Save predictions to CSV and upload to S3"""
        try:
            # Save locally
            os.makedirs('predictions', exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'predictions/predictions_{timestamp}.csv'
            
            df_predictions = pd.DataFrame({
                'prediction': predictions,
                'timestamp': datetime.now()
            })
            df_predictions.to_csv(filename, index=False)
            logger.info(f"Predictions saved to {filename}")
            
            # Upload to S3 (optional)
            try:
                self.upload_to_s3(filename)
            except Exception as e:
                logger.warning(f"S3 upload failed (optional): {str(e)}")
        
        except Exception as e:
            logger.error(f"Error saving predictions: {str(e)}")
            raise
    
    def upload_to_s3(self, filename):
        """Upload predictions to S3 bucket"""
        try:
            s3_bucket = os.getenv('S3_BUCKET', 'forest-predictions')
            
            s3_client = boto3.client('s3')
            s3_client.upload_file(filename, s3_bucket, os.path.basename(filename))
            logger.info(f"File uploaded to S3: {s3_bucket}/{os.path.basename(filename)}")
        except Exception as e:
            logger.warning(f"S3 upload failed: {str(e)}")
            raise
