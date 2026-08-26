from celery import shared_task
from django.core.cache import cache
import random
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

@shared_task
def OtpCreateTask(username):
    otp=random.randint(100000, 999999)
    user_data=get_object_or_404(User, username=username)
    cache.set(f"otp_for_user:{user_data.id}", otp, timeout=500)
    return f"otp created for username: {username}, otp: {otp}"