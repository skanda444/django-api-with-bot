from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Public endpoint (no authentication required)
    path('public/', views.public_api, name='public_api'),
    
    # Secure endpoint (JWT authentication required)
    path('secure/', views.secure_api, name='secure_api'),
    
    # User profile endpoints
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    
    # Posts endpoints
    path('posts/', views.PostListCreateView.as_view(), name='post_list_create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
]