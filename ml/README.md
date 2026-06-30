# Machine Learning Package

This directory contains the real estate price prediction code and artifacts.

## Files

- `train.py`: loads `dataset/housing.csv`, preprocesses features, trains multiple regressors, evaluates them, and writes model files.
- `predict.py`: loads `models/best_model.pkl` lazily and exposes `predict_price(features)`.
- `dataset/`: training CSV data.
- `models/`: serialized scikit-learn model files.
- `notebooks/`: exploratory or training notebook.

## Prediction Features

The prediction helper expects area, bedrooms, bathrooms, stories, six yes/no amenity fields, parking, preferred-area status, and furnishing status.
