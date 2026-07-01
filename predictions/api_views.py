from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Prediction
from .serializers import PredictionSerializer
from .views import parse_prediction_features
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ml'))


class PredictionCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            features = parse_prediction_features(request.data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
