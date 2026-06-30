"""
predict.py — Called by Django to generate a property price prediction.
Usage:
    from ml.predict import predict_price
    price = predict_price({'area': 3000, 'bedrooms': 3, ...})
"""
import os
import joblib
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'best_model.pkl')

_model = None

def _load_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found at {MODEL_PATH}. Run 'python ml/train.py' first."
            )
        _model = joblib.load(MODEL_PATH)
    return _model

def predict_price(features: dict) -> float:
    """
    Accepts a dict with keys:
      area, bedrooms, bathrooms, stories,
      mainroad, guestroom, basement, hotwaterheating,
      airconditioning, parking, prefarea, furnishingstatus
    Returns predicted price as float.
    """
    binary_map = {'yes': 1, 'no': 0}
    furnish_map = {'furnished': 2, 'semi-furnished': 1, 'unfurnished': 0}

    input_vector = [
        int(features['area']),
        int(features['bedrooms']),
        int(features['bathrooms']),
        int(features['stories']),
        binary_map.get(features['mainroad'], 0),
        binary_map.get(features['guestroom'], 0),
        binary_map.get(features['basement'], 0),
        binary_map.get(features['hotwaterheating'], 0),
        binary_map.get(features['airconditioning'], 0),
        int(features['parking']),
        binary_map.get(features['prefarea'], 0),
        furnish_map.get(features['furnishingstatus'], 0),
    ]

    model = _load_model()
    prediction = model.predict(np.array(input_vector).reshape(1, -1))
    return float(prediction[0])
