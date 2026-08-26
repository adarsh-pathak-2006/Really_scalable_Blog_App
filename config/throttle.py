from rest_framework.throttling import UserRateThrottle

class RegistrationThrottle(UserRateThrottle):
    rate="20/hour"

class TokenObtainThrottle(UserRateThrottle):
    rate="40/hour"

class TokenRefreshThrottle(UserRateThrottle):
    rate="10/hour"