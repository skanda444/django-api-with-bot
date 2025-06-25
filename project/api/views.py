from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.utils import timezone
from .models import UserProfile, Post
from .serializers import UserProfileSerializer, PostSerializer, PublicMessageSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def public_api(request):
    """
    Public API endpoint that returns a simple JSON message.
    No authentication required.
    """
    data = {
        'message': 'Welcome to our Django REST API!',
        'timestamp': timezone.now(),
        'version': '1.0.0',
        'status': 'active',
        'endpoints': {
            'public': '/api/public/',
            'secure': '/api/secure/',
            'posts': '/api/posts/',
            'profile': '/api/profile/',
        }
    }
    
    serializer = PublicMessageSerializer(data)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def secure_api(request):
    """
    Secure API endpoint that requires JWT authentication.
    Returns user-specific data.
    """
    user = request.user
    
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    # Get user's posts
    user_posts = Post.objects.filter(author=user)
    
    data = {
        'message': f'Hello {user.username}! This is your secure data.',
        'user_info': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
        },
        'profile': UserProfileSerializer(profile).data,
        'posts_count': user_posts.count(),
        'recent_posts': PostSerializer(user_posts[:5], many=True).data,
        'timestamp': timezone.now(),
    }
    
    return Response(data, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update user profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class PostListCreateView(generics.ListCreateAPIView):
    """
    List all posts or create a new post.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a post.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)