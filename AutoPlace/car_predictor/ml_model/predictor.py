import joblib
import json
import numpy as np
import pandas as pd
import os
from django.conf import settings

class CarPricePredictor:
    def __init__(self):
        model_path = os.path.join(settings.BASE_DIR, 'car_predictor', 'ml_model', 'car_price_predictor.pkl')
        info_path = os.path.join(settings.BASE_DIR, 'car_predictor', 'ml_model', 'model_info.json')
        
        self.model = joblib.load(model_path)
        with open(info_path, 'r') as f:
            self.model_info = json.load(f)
    
    def predict_price(self, input_data):
        """Predict car price from input data"""
        
        input_df = pd.DataFrame([input_data])
        prediction = self.model.predict(input_df)[0]
        
        return round(prediction, 2)


predictor = CarPricePredictor()