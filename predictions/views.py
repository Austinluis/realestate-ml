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

INTEGER_FIELDS = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking']
CHOICE_DEFAULTS = {
    'mainroad': 'no',
    'guestroom': 'no',
    'basement': 'no',
    'hotwaterheating': 'no',
    'airconditioning': 'no',
    'prefarea': 'no',
    'furnishingstatus': 'unfurnished',
}

def parse_prediction_features(data):
    features = {}
    for field in INTEGER_FIELDS:
        value = data.get(field)
        if value in (None, ''):
            raise ValueError(f'{field} is required.')
        features[field] = int(value)

    for field, default in CHOICE_DEFAULTS.items():
        features[field] = data.get(field) or default

    return features

@login_required
def predict_view(request):
    properties = Property.objects.filter(owner=request.user)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, Exception):
            data = request.POST.dict()

        try:
            features = parse_prediction_features(data)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

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

    selected_property = None
    prop_id = request.GET.get('property_id')
    if prop_id:
        try:
            selected_property = properties.get(pk=prop_id)
        except Property.DoesNotExist:
            selected_property = None

    return render(request, 'predictions/predict.html', {
        'properties': properties,
        'selected_property': selected_property,
    })

@login_required
def prediction_history(request):
    predictions = Prediction.objects.filter(user=request.user)
    return render(request, 'predictions/history.html', {'predictions': predictions})
