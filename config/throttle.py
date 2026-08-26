from rest_framework.throttling import UserRateThrottle

class RegistrationThrottle(UserRateThrottle):
    rate="20/hour"