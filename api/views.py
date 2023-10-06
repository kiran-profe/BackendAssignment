from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import User, Post
from .serializers import UserRegistrationSerializer, UserLoginSerializer, PostSerializer, PostGetSerializer
from django.contrib.auth import authenticate
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterUser(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)

class LoginUser(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
        
class CreateNewPost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        newPostSerializer = PostSerializer(data=request.data)
        if newPostSerializer.is_valid():
            
            newPostSerializer.save(user=self.request.user)
            return Response(newPostSerializer.data)
        else:
            return Response(newPostSerializer.errors)

class PostList(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticated]
    page_size = 1

    def get(self, request):
        user = User.objects.get(id=self.request.user.id)
        PostList = user.post_set.all()
        results = self.paginate_queryset(PostList, request, view=self)
        serializer = PostGetSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)
    
class UpdatePost(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        post = Post.objects.get(id=pk)
        if post.user == request.user:
            updatePostSerializer = PostSerializer(post, data=request.data)
            if updatePostSerializer.is_valid():
                updatePostSerializer.save()
                return Response(updatePostSerializer.data)
            else:
                return Response(updatePostSerializer.errors)
        else:
            return Response({"msg": "You cant update this!"})
        
class DeletePost(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        post = Post.objects.get(id=pk)
        if post.user == request.user:
            post.delete()
            return Response({"deleted": pk})
        else:
            return Response({"msg": "You cant delete this!"})