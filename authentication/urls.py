from django.urls import path
from .views import CustomTokenObtainView, CustomTokenRefreshView, RegisterAPI, OtpVerificationAPI, MyProfileAPI

urlpatterns = [
    path('token/', CustomTokenObtainView.as_view(), name='token_obtain_view'),
    path('register-user/', RegisterAPI.as_view(), name='register'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh_view'),
    path('otp-verify/<int:username>/', OtpVerificationAPI.as_view(), name='otp_verification'),
    path('my-profile/', MyProfileAPI.as_view(), name='my_profile'),
]
