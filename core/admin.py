from django.contrib import admin
from .models import Profile, Blog, Comment

admin.site.register(Profile)
admin.site.register(Blog)
admin.site.register(Comment)