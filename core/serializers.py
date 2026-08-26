from rest_framework.serializers import ModelSerializer
from .models import Blog, Comment
from authentication.serializers import ProfileGetSerializer

class BlogGetSerializer(ModelSerializer):
    user=ProfileGetSerializer(read_only=True)
    class Meta:
        model=Blog
        fields=['user', 'title', 'content']

class BlogSerializer(ModelSerializer):
    user=ProfileGetSerializer(read_only=True)
    class Meta:
        model=Blog
        fields='__all__'

class CommentSerializer(ModelSerializer):
    blog=BlogGetSerializer(read_only=True)
    user=ProfileGetSerializer(read_only=True)
    class Meta:
        model=Comment
        fields='__all__'
