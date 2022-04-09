from rest_framework import response, status, views
from rest_framework.settings import api_settings
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated 
from django.contrib.auth.models import User

from .serializers import RegisterDataSerializer, PostSerializer, CommentSerializer
from .models import Post, Comment

class RegisterView(views.APIView):
    serializer_class = RegisterDataSerializer
    permission_classes = () # needed for unregistered users access

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

class PostView(views.APIView, LimitOffsetPagination):
    serializer_class = PostSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get(self, request, id=None):
        if id:
            return self.retrieve(id)
        else:
            return self.list(request)

    def post(self, request):
        data = request.data.copy()
        data['author'] = request.user
        serializer = self.serializer_class(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, id):
        try:
            post = Post.objects.get(id=id)
        except:
            return response.Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(post)
        return response.Response(serializer.data)

    def list(self, request):
        queryset = Post.objects.all().order_by('-date_added')
        posts = self.paginate_queryset(queryset, request, view=self)
        max_body_len = 400

        for post in posts:
            if len(post.body) > max_body_len:
                post.body = post.body[:max_body_len] + '...'

        serializer = self.serializer_class(posts, many=True)
        return self.get_paginated_response(serializer.data)

class CommentView(views.APIView, LimitOffsetPagination):
    serializer_class = CommentSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get(self, request, post_id=None):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return response.Response(status=status.HTTP_404_NOT_FOUND)

        queryset = Comment.objects.filter(post=post).order_by('-date_added')
        comments = self.paginate_queryset(queryset, request, view=self)
        serializer = self.serializer_class(comments, many=True)
        
        return self.get_paginated_response(serializer.data)

    def post(self, request, post_id=None):
        data = request.data.copy()
        data['author'] = request.user
        data['post'] = post_id

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

class UserView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = User.objects.get(username=request.user)
        return response.Response({'username': user.username})

class LogoutView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)