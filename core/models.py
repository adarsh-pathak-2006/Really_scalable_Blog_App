from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField()
    profile_picture=models.ImageField(upload_to='pfps/', null=True)
    bio=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.name=f"{self.user.first_name} {self.user.last_name}"
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Blog(models.Model):
    user=models.ForeignKey(Profile, on_delete=models.CASCADE)
    title=models.CharField(max_length=300)
    content=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"blog of title {self.title} created by {self.user.name}"

class Comment(models.Model):
    blog=models.ForeignKey(Blog, on_delete=models.CASCADE)
    user=models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment on {self.blog.title} done by {self.user.name}"