# Trained ML Models

This directory stores serialized scikit-learn models written by `ml/train.py`.

Current model artifacts:

- `best_model.pkl`: model loaded by the Django prediction flow.
- `linear_regression.pkl`: trained linear regression model.
- `decision_tree.pkl`: trained decision tree regressor.
- `random_forest.pkl`: trained random forest regressor.

If these files are regenerated, keep the dependency versions compatible with the deployment environment.
