"""
API routing for Project Horizon.
Central hub for all API endpoints.
"""
from django.urls import path, include

app_name = 'api'

urlpatterns = [
    # Add app-specific endpoints here
    # path('users/', include('apps.users.urls', namespace='users')),
    # path('posts/', include('apps.posts.urls', namespace='posts')),
]
