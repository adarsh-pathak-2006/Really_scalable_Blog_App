from django.shortcuts import get_object_or_404
from .serializers import ProfileSerializer, RegisterSerializer
from .models import Profile
from django.contrib.auth.models import User
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import View
from django.db.models import Q
from rest_framework.response import Response

class RegisterAPI(View):
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
            user=User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
            Profile.objects.create(user=user)
            return Response({'message':'registration successfull'}, status=201)
        return Response(serial.errors, status=400)

class MyProfileAPI(RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

