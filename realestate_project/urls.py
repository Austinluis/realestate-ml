from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('properties/', include('properties.urls')),
    path('predictions/', include('predictions.urls')),
    path('dashboard/', include('accounts.urls_dashboard')),
    path('', include('accounts.urls')),
]
