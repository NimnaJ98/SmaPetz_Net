from django.urls import path
from .views import (
    profile_test_view,
    received_requests_view,

)

app_name = 'profiles'

urlpatterns = [
    path('profile/', profile_test_view, name='profile-test'),
    path('requests/', received_requests_view, name='user-requests'),
    
]