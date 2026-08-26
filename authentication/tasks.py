from celery import shared_task
from django.core.cache import cache
import random
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import time

@shared_task
def OtpCreateTask(username):
    otp=random.randint(100000, 999999)
    time.sleep(10)
    user_data=get_object_or_404(User, username=username)
    cache.set(f"otp_for_user:{user_data.id}", str(otp), timeout=500)
    return f"otp created for username: {username}, otp: {otp}"