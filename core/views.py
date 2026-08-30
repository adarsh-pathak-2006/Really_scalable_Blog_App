from django.shortcuts import get_object_or_404
from .models import Blog, Comment
from .serializers import BlogSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from authentication.models import Profile
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination

class AllBlogAPI(ListAPIView):
    queryset = Blog.objects.select_related('user__user').all()
    serializer_class = BlogSerializer

    @method_decorator(cache_page(300))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class AllBlogsIndividualAPI(APIView):
    def get(self, request, pk):
        data = get_object_or_404(Blog.objects.select_related('user__user'), id=pk)
        serial = BlogSerializer(data)
        return Response(serial.data, status=200)

class MyBlogsAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer

    def get_queryset(self):
        profile_data = get_object_or_404(Profile, user=self.request.user)
        return Blog.objects.select_related('user__user').filter(user=profile_data)

class BlogCreateAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serial = BlogSerializer(data=request.data)
        if serial.is_valid():
            profile_data = get_object_or_404(Profile, user=request.user)
            serial.save(user=profile_data)
            return Response(serial.data, status=201)
        return Response(serial.errors, status=400)

class MyBlogsDetailAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        profile_data = get_object_or_404(Profile, user=request.user)
        data = get_object_or_404(Blog.objects.select_related('user__user'), user=profile_data, id=pk)
        serial = BlogSerializer(data)
        return Response(serial.data, status=200)
 
    def put(self, request, pk):
        profile_data = get_object_or_404(Profile, user=request.user)
        instance = get_object_or_404(Blog, id=pk, user=profile_data)
        serial = BlogSerializer(instance, data=request.data, partial=True)
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=200)
        return Response(serial.errors, status=400)

    def delete(self, request, pk):
        profile_data = get_object_or_404(Profile, user=request.user)
        instance = get_object_or_404(Blog, id=pk, user=profile_data)
        instance.delete()
        return Response(status=204)                

class CommentAPI(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]
        
    def get(self, request, pk):
        blog_data = get_object_or_404(Blog, id=pk)
        data = Comment.objects.select_related('user__user', 'blog').filter(blog=blog_data)
        
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(data, request)
        serial = CommentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serial.data)

    def post(self, request, pk):
        serial = CommentSerializer(data=request.data)
        if serial.is_valid():
            blog_data = get_object_or_404(Blog, id=pk)
            profile_data = get_object_or_404(Profile, user=request.user)
            serial.save(blog=blog_data, user=profile_data)
            return Response(serial.data, status=201)
        return Response(serial.errors, status=400)
