from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture=models.ImageField(upload_to='pfps/', null=True)
    bio=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

    @property
    def name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return self.name
