# Predictions App

This Django app handles property price prediction requests and prediction history.

## Responsibilities

- Defines the `Prediction` model in `models.py`.
- Stores a snapshot of input features for each prediction.
- Calls the ML prediction helper from `ml/predict.py`.
- Provides the prediction form and history pages in `views.py`.
- Provides prediction API endpoints in `api_views.py`.
- Serializes prediction history in `serializers.py`.
- Registers prediction records in Django admin through `admin.py`.
- Contains tests for prediction access, history, and ownership behavior.

## Prediction Flow

The browser posts property feature values to `/predictions/`. The view validates numeric fields, calls `predict_price()`, saves the result, and returns JSON for the page to display.
