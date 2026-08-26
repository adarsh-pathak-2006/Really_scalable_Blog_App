from django.shortcuts import get_object_or_404, redirect
from .serializers import ProfileSerializer, RegisterSerializer, OtpVerificationSerializer
from .models import Profile
from django.contrib.auth.models import User
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response
from django.core.cache import cache
from .tasks import OtpCreateTask
from config.throttle import RegistrationThrottle
from rest_framework.permissions import IsAuthenticated

class RegisterAPI(APIView):
    throttle_classes=[RegistrationThrottle]
    def post(self, request):
        serial=RegisterSerializer(data=request.data)
        if serial.is_valid():
            username=serial.validated_data['username']
            email=serial.validated_data['email']
            first_name=serial.validated_data['first_name']
            last_name=serial.validated_data['last_name']
            password=serial.validated_data['password']

            if User.objects.filter(Q(username=username) | Q(email=email)).exists():
                return Response({'message':'username  or email already exists'}, status=400)
            cache.set(f"session_cache_{username}", {'username':username, 'email':email, 'first_name':first_name, 'last_name':last_name, 'password':password}, timeout=800)
            OtpCreateTask.delay(username=username)
            # user=User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
            # Profile.objects.create(user=user)
            return redirect('otp_verification')
        return Response(serial.errors, status=400)

class OtpVerificationAPI(APIView):
    throttle_classes=[RegistrationThrottle]
    def post(self, request, username):
        serial=OtpVerificationSerializer(data=request.data)
        if serial.is_valid():
            otp=serial.validated_data['otp']
            user_data=get_object_or_404(User, username=username)
            generated_otp=cache.get(f"otp_for_user:{user_data.id}")
            if otp==generated_otp:
                cached_session=cache.get(f"session_cache_{username}")
                user=User.objects.create_user(username=cached_session.get('username'), email=cached_session.get('email'), first_name=cached_session.get('email'), last_name=cached_session.get('last_name'), password=cached_session.get('password'))
                Profile.objects.create(user=user)
                return Response({'message':'user registration successfull'}, status=201)
            cache.delete(f"session_cache_{username}")
            return Response({'failed':'you entered incorrect OTP..try registration again'}, status=400)


class MyProfileAPI(RetrieveUpdateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=ProfileSerializer

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)
