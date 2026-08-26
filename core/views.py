from django.shortcuts import get_object_or_404
from .models import Blog, Comment
from .serializers import BlogSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from authentication.models import Profile
from rest_framework.permissions import IsAuthenticated

class AllBlogAPI(APIView):
    def get(self, request):
        cached_data=cache.get("all_blogs")
        if cached_data:
            return Response(cached_data, status=200)
        data=Blog.objects.all()
        serial=BlogSerializer(data, many=True)
        cache.set("all_blogs", serial.data, timeout=300)
        return Response(serial.data, status=200)

class AllBlogsIndividualAPI(APIView):
    def get(self, request, pk):
        cached_data=cache.get(f"all_blogs_{pk}")
        if cached_data:
            return Response(cached_data, status=200)
        data=get_object_or_404(Blog, id=pk)
        serial=BlogSerializer(data)
        cache.set(f"all_blogs_{pk}", serial.data, timeout=300)
        return Response(serial.data, status=200)

class MyBlogsAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        profile_data=get_object_or_404(Profile, user=request.user)
        cached_data=cache.get(f"blogs_profileid:{profile_data.id}")
        if cached_data:
            return Response(cached_data, status=200)
        data=Blog.objects.filter(user=profile_data)
        serial=BlogSerializer(data, many=True)
        cache.set(f"blogs_profileid:{profile_data.id}", serial.data, timeout=300)
        return Response(serial.data, status=200)

class BlogCreateAPI(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        serial=BlogSerializer(data=request.data)
        if serial.is_valid():
            profile_data=get_object_or_404(Profile, user=request.user)
            serial.save(user=profile_data)
            cache.delete("all_blogs")
            cache.delete(f"blogs_profileid:{profile_data.id}")
            return Response(serial.data, status=201)
        return Response(serial.errors, status=400)

class MyBlogsDetailAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, pk):
        profile_data=get_object_or_404(Profile, user=request.data)
        cached_data=cache.get(f"blogs_profileid:{profile_data.id}_{pk}")
        if cached_data:
            return Response(cached_data, status=200)
        data=get_object_or_404(Blog, user=profile_data, id=pk)
        serial=BlogSerializer(data)
        cache.set(f"blogs_profileid:{profile_data.id}_{pk}", serial.data, timeout=300)
        return Response(serial.data, status=200)
 
    def put(self, request, pk):
        profile_data=get_object_or_404(Profile, user=request.user)
        instance=get_object_or_404(Blog, id=pk, user=profile_data)
        serial=BlogSerializer(instance, data=request.data, partial=True)
        if serial.is_valid():
            serial.save()
            cache.delete(f"all_blogs_{pk}")
            cache.delete("all_blogs")
            cache.delete(f"blogs_profileid:{profile_data.id}")
            cache.delete(f"blogs_profileid:{profile_data.id}_{pk}")
            return Response(serial.data, status=200)
        return Response(serial.errors, status=400)

    def delete(self, request, pk):
        profile_data=get_object_or_404(Profile, user=request.user)
        instance=get_object_or_404(Blog, id=pk, user=profile_data)
        instance.delete()
        cache.delete(f"all_blogs_{pk}")
        cache.delete("all_blogs")
        cache.delete(f"blogs_profileid:{profile_data.id}")
        cache.delete(f"blogs_profileid:{profile_data.id}_{pk}")
        return Response(status=204)                

class CommentAPI(APIView):
    def get(self, request, pk):
        cached_data=cache.get(f"comments_on_blogid:{pk}")
        if cached_data:
            return Response(cached_data, status=200)
        blog_data=get_object_or_404(Blog, id=pk)
        profile_data=get_object_or_404(Profile, user=request.user)
        data=Comment.objects.filter(blog=blog_data, user=profile_data)
        serial=CommentSerializer(data, many=True)
        cache.set(f"comments_on_blogid:{pk}", serial.data, timeout=300)
        return Response(serial.data, status=200)

    def post(self, request, pk):
        serial=CommentSerializer(data=request.data)
        if serial.is_valid():
            blog_data=get_object_or_404(Blog, id=pk)
            profile_data=get_object_or_404(Profile, user=request.user)
            serial.save(blog=blog_data, user=profile_data)
            cache.delete(f"comments_on_blogid:{pk}")
            return Response(serial.data, status=201)
        return Response(serial.errors, status=400)        
