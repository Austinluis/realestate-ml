from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Property
from .serializers import PropertySerializer


class PropertyListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        properties = Property.objects.filter(owner=request.user)
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertyDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_property(self, pk, user):
        return get_object_or_404(Property, pk=pk, owner=user)

    def get(self, request, pk):
        prop = self._get_property(pk, request.user)
        return Response(PropertySerializer(prop).data)

    def put(self, request, pk):
        prop = self._get_property(pk, request.user)
        serializer = PropertySerializer(prop, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        prop = self._get_property(pk, request.user)
        prop.delete()
        return Response({'message': 'Property deleted.'}, status=status.HTTP_204_NO_CONTENT)
