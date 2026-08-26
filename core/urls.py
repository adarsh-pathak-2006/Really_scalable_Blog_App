from django.urls import path
from .views import AllBlogAPI, AllBlogsIndividualAPI, MyBlogsAPI, BlogCreateAPI, MyBlogsDetailAPI, CommentAPI

urlpatterns = [
    path('all-blogs/', AllBlogAPI.as_view()),
    path('all-blogs/<int:pk>/', AllBlogsIndividualAPI.as_view()),
    path('my-blogs/', MyBlogsAPI.as_view()),
    path('my-blogs/<int:pk>/', MyBlogsDetailAPI.as_view()),
    path('blog-create/', BlogCreateAPI.as_view()),
    path('comment/<int:pk>/', CommentAPI.as_view()),
]
