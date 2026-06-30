from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'location', 'area', 'bedrooms', 'listed_price', 'created_at']
    list_filter = ['furnishingstatus', 'airconditioning', 'prefarea']
    search_fields = ['title', 'location', 'owner__email']
    readonly_fields = ['created_at', 'updated_at']
