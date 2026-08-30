from django.shortcuts import get_object_or_404, redirect
from .serializers import ProfileSerializer, RegisterSerializer
from .models import Profile
from django.contrib.auth.models import User
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response
from config.throttle import RegistrationThrottle, TokenObtainThrottle, TokenRefreshThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.db import transaction

class CustomTokenObtainView(TokenObtainPairView):
    throttle_classes=[TokenObtainThrottle]

class CustomTokenRefreshView(TokenRefreshView):
    throttle_classes=[TokenRefreshThrottle]

class RegisterAPI(APIView):
    throttle_classes=[RegistrationThrottle]
    def post(self, request):
        serial=RegisterSerializer(data=request.data)
        if serial.is_valid():
            username=serial.validated_data['username']
            email=serial.validated_data['email']
            first_name=serial.validated_data.get('first_name')
            last_name=serial.validated_data.get('last_name')
            password=serial.validated_data['password']

            with transaction.atomic():
                user=User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
                Profile.objects.create(user=user)
            return Response({'message':'user registered successfully'}, status=201)
        return Response(serial.errors, status=400)
        
class MyProfileAPI(RetrieveUpdateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=ProfileSerializer

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)
