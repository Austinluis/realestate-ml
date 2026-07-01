from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .models import User
from .serializers import UserSerializer


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        required = ['username', 'email', 'password']
        for field in required:
            if not data.get(field):
                return Response({'error': f'{field} is required.'}, status=status.HTTP_400_BAD_REQUEST)
        email = data['email'].strip().lower()
        username = data['username'].strip()
        if User.objects.filter(email__iexact=email).exists():
            return Response({'error': 'An account with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username__iexact=username).exists():
            return Response({'error': 'An account with this username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=data['password'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        identifier = request.data.get('identifier') or request.data.get('email')
        password = request.data.get('password')
        if not identifier or not password:
            return Response({'error': 'Username/email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        auth_identifier = identifier.strip()
        if '@' not in auth_identifier:
            matched_user = User.objects.filter(username__iexact=auth_identifier).first()
            if matched_user:
                auth_identifier = matched_user.email
        user = authenticate(request, username=auth_identifier, password=password)
        if user:
            login(request, user)
            return Response({'message': 'Login successful.', 'user': UserSerializer(user).data})
        return Response({'error': 'Invalid username/email or password.'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully.'})


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        user = request.user
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.save()
        return Response(UserSerializer(user).data)
