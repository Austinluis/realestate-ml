"""
ML Training Script — Real Estate Price Prediction
Run: python ml/train.py
Requires: ml/dataset/housing.csv (download from Kaggle)
"""
import os
import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, 'dataset', 'housing.csv')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

def load_and_preprocess(path):
    df = pd.read_csv(path)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

    # Encode binary yes/no columns
    binary_cols = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']
    for col in binary_cols:
        df[col] = df[col].map({'yes': 1, 'no': 0})

    # Encode furnishingstatus
    furnish_map = {'furnished': 2, 'semi-furnished': 1, 'unfurnished': 0}
    df['furnishingstatus'] = df['furnishingstatus'].map(furnish_map)

    features = ['area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 'guestroom',
                'basement', 'hotwaterheating', 'airconditioning', 'parking', 'prefarea', 'furnishingstatus']
    target = 'price'

    X = df[features]
    y = df[target]
    return X, y

def evaluate(name, model, X_test, y_test):
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    print(f"\n{name}:")
    print(f"  MAE:  {mae:,.2f}")
    print(f"  RMSE: {rmse:,.2f}")
    print(f"  R²:   {r2:.4f}")
    return r2, model

def main():
    X, y = load_and_preprocess(DATASET_PATH)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        'Linear Regression': LinearRegression(),
        'Decision Tree': DecisionTreeRegressor(random_state=42),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
    }

    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        r2, trained = evaluate(name, model, X_test, y_test)
        results[name] = (r2, trained)

    # Save all models
    joblib.dump(results['Linear Regression'][1], os.path.join(MODELS_DIR, 'linear_regression.pkl'))
    joblib.dump(results['Decision Tree'][1], os.path.join(MODELS_DIR, 'decision_tree.pkl'))
    joblib.dump(results['Random Forest'][1], os.path.join(MODELS_DIR, 'random_forest.pkl'))

    # Save best model
    best_name = max(results, key=lambda k: results[k][0])
    best_model = results[best_name][1]
    joblib.dump(best_model, os.path.join(MODELS_DIR, 'best_model.pkl'))
    print(f"\nBest model: {best_name} (R²={results[best_name][0]:.4f})")
    print("All models saved to ml/models/")

if __name__ == '__main__':
    main()
