import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Prediction
from properties.models import Property
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ml'))

@login_required
def predict_view(request):
    properties = Property.objects.filter(owner=request.user)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, Exception):
            data = request.POST.dict()

        features = {
            'area': int(data.get('area', 0)),
            'bedrooms': int(data.get('bedrooms', 0)),
            'bathrooms': int(data.get('bathrooms', 0)),
            'stories': int(data.get('stories', 0)),
            'mainroad': data.get('mainroad', 'no'),
            'guestroom': data.get('guestroom', 'no'),
            'basement': data.get('basement', 'no'),
            'hotwaterheating': data.get('hotwaterheating', 'no'),
            'airconditioning': data.get('airconditioning', 'no'),
            'parking': int(data.get('parking', 0)),
            'prefarea': data.get('prefarea', 'no'),
            'furnishingstatus': data.get('furnishingstatus', 'unfurnished'),
        }

        try:
            from predict import predict_price
            predicted = predict_price(features)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        # Save prediction record
        prop_id = data.get('property_id')
        prop = None
        if prop_id:
            try:
                prop = Property.objects.get(pk=prop_id, owner=request.user)
            except Property.DoesNotExist:
                pass

        prediction = Prediction.objects.create(
            user=request.user,
            property=prop,
            predicted_price=predicted,
            **features
        )

        return JsonResponse({'predicted_price': predicted, 'prediction_id': prediction.id})

    return render(request, 'predictions/predict.html', {'properties': properties})

@login_required
def prediction_history(request):
    predictions = Prediction.objects.filter(user=request.user)
    return render(request, 'predictions/history.html', {'predictions': predictions})
