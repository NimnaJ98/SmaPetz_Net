from urllib.request import url2pathname
from django.urls import path
from .views import (
    profile_test_view,
    received_requests_view,
    profile_list_view,
    profiles_to_request,
    ProfileList
)

app_name = 'profiles'

urlpatterns = [
    path('profile/', profile_test_view, name='profile-test'),
    path('requests/', received_requests_view, name='user-requests'),
    path('all-profiles/', ProfileList.as_view(), name='all-profiles'),
    path('to-request/', profiles_to_request, name='available-requests'),
]
