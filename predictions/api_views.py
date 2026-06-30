from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Prediction
from .serializers import PredictionSerializer
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ml'))


class PredictionCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        features = {
            'area': int(request.data.get('area', 0)),
            'bedrooms': int(request.data.get('bedrooms', 0)),
            'bathrooms': int(request.data.get('bathrooms', 0)),
            'stories': int(request.data.get('stories', 0)),
            'mainroad': request.data.get('mainroad', 'no'),
            'guestroom': request.data.get('guestroom', 'no'),
            'basement': request.data.get('basement', 'no'),
            'hotwaterheating': request.data.get('hotwaterheating', 'no'),
            'airconditioning': request.data.get('airconditioning', 'no'),
            'parking': int(request.data.get('parking', 0)),
            'prefarea': request.data.get('prefarea', 'no'),
            'furnishingstatus': request.data.get('furnishingstatus', 'unfurnished'),
        }
        try:
            from predict import predict_price
            predicted = predict_price(features)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        prediction = Prediction.objects.create(
            user=request.user,
            predicted_price=predicted,
            **features
        )
        return Response({
            'predicted_price': predicted,
            'prediction_id': prediction.id,
        }, status=status.HTTP_201_CREATED)


class PredictionHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        predictions = Prediction.objects.filter(user=request.user)
        serializer = PredictionSerializer(predictions, many=True)
        return Response(serializer.data)
