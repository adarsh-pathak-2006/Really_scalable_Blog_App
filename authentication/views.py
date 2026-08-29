from django.shortcuts import get_object_or_404, redirect
from .serializers import ProfileSerializer, RegisterSerializer, OtpVerificationSerializer, PasswordSetupSerializer
from .models import Profile
from django.contrib.auth.models import User
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response
from django.core.cache import cache
from .tasks import OtpCreateTask
from config.throttle import RegistrationThrottle, TokenObtainThrottle, TokenRefreshThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
            first_name=serial.validated_data['first_name']
            last_name=serial.validated_data['last_name']
            cache.set(f"session_cache_username:{username}", {'username':username, 'email':email, 'first_name':first_name, 'last_name':last_name}, timeout=300) 
            OtpCreateTask.delay(username=username)
            return Response({'message':'otp is generated..enter the correct otp to move ahead'}, status=201)
        return Response(serial.errors, status=400)

class OtpVerificationAPI(APIView):
    throttle_classes=[RegistrationThrottle]
    def post(self, request, username):
        serial=OtpVerificationSerializer(data=request.data)
        if serial.is_valid():
            otp=serial.validated_data['otp']
            generated_otp=cache.get(f"otp_for_user:{username}")
            if otp==generated_otp:
                return Response({'message':'otp_verified'}, status=200)
            return Response({'message':'wrong otp entered..retry'}, status=400)
        return Response(serial.errors, status=400)
   
class PasswordSetupAPI(APIView):
    def post(self, request):
        
        
class MyProfileAPI(RetrieveUpdateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=ProfileSerializer

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)
