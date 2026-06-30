from django.contrib import admin
from .models import Prediction

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'predicted_price', 'model_used', 'created_at']
    list_filter = ['model_used']
    search_fields = ['user__email']
