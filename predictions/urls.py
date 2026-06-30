from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    # Template views
    path('', views.predict_view, name='predict'),
    path('history/', views.prediction_history, name='prediction_history'),
    # REST API endpoints
    path('api/predict/', api_views.PredictionCreateAPIView.as_view(), name='api_predict'),
    path('api/history/', api_views.PredictionHistoryAPIView.as_view(), name='api_prediction_history'),
]
