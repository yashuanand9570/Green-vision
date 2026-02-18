import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

class TrainPipeline:
    def __init__(self, data_path:str, model_output_path:str):
        self.data_path = data_path
        self.model_output_path = model_output_path
        self.model = None

    def load_data(self):
        data = pd.read_csv(self.data_path)
        return data

    def preprocess_data(self, data:pd.DataFrame):
        # Example preprocessing: filling missing values and splitting features and labels
        data.fillna(method='ffill', inplace=True)
        X = data.drop('target', axis=1)
        y = data['target']
        return X, y

    def train_model(self, X:pd.DataFrame, y:pd.Series):
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model = RandomForestClassifier()
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_val)
        accuracy = accuracy_score(y_val, predictions)
        f1 = f1_score(y_val, predictions, average='weighted')
        print(f'Accuracy: {accuracy}, F1 Score: {f1}')

    def save_model(self):
        joblib.dump(self.model, self.model_output_path)

    def run(self):
        data = self.load_data()
        X, y = self.preprocess_data(data)
        self.train_model(X, y)
        self.save_model()