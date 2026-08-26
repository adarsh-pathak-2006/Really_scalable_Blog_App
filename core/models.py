from django.db import models
from authentication.models import Profile


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