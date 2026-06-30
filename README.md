# EstateIQ

EstateIQ is a Django-based real estate management and price prediction system. It lets authenticated users manage property listings, upload property photos, and run machine-learning price predictions from property features.

Deployed site: https://realestate-ml-production.up.railway.app

## Main Features

- Email-based user registration, login, logout, and profile APIs.
- User dashboard with property and prediction activity.
- Property CRUD for owned listings.
- Property photo upload and display.
- ML-powered price prediction from housing features.
- Prediction history saved per user.
- Django REST Framework API endpoints alongside server-rendered pages.
- WhiteNoise static-file serving for deployment.

## Technology Stack

- Python and Django 4.2 for the backend web framework.
- Django Templates for server-rendered HTML.
- Django REST Framework for API endpoints.
- MySQL as the configured production/local database engine.
- scikit-learn, pandas, numpy, scipy, and joblib for model training and prediction.
- Bootstrap 5 and Bootstrap Icons through CDN.
- Custom CSS in `static/css/style.css`.
- WhiteNoise for compressed static assets.
- Gunicorn for production WSGI serving.
- Railway deployment via `Procfile` and `runtime.txt`.

## Project Structure

- `accounts/`: custom user model, authentication views, dashboard, auth APIs, and tests.
- `properties/`: property listing model, CRUD views, APIs, upload handling, and tests.
- `predictions/`: prediction model, prediction form/history views, prediction APIs, and tests.
- `ml/`: training script, prediction helper, dataset, notebook, and trained model files.
- `realestate_project/`: Django project settings, root URL routing, and WSGI entry point.
- `templates/`: shared and page-specific Django templates.
- `static/`: source CSS, JavaScript, and static assets.
- `media/`: local uploaded files such as property photos.
- `staticfiles/`: generated collectstatic output; not source code.

## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` from `.env.example` and set database credentials.
4. Ensure MySQL is running and the configured database exists.
5. Apply migrations:

   ```bash
   python manage.py migrate
   ```

6. Run the server:

   ```bash
   python manage.py runserver
   ```

## Machine Learning

The app loads `ml/models/best_model.pkl` in `ml/predict.py` and predicts prices using these features:

- area
- bedrooms
- bathrooms
- stories
- mainroad
- guestroom
- basement
- hotwaterheating
- airconditioning
- parking
- prefarea
- furnishingstatus

To retrain models, use:

```bash
python ml/train.py
```

The script expects `ml/dataset/housing.csv` and writes trained models to `ml/models/`.

## Deployment Notes

The `Procfile` runs migrations, collects static files, then starts Gunicorn. Uploaded media files are stored under `MEDIA_ROOT`; on Railway or similar platforms, persistent media storage should be configured if uploaded photos must survive redeploys.

## Useful Commands

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py test
python manage.py collectstatic --noinput
```
