from urllib.request import url2pathname
from django.urls import path
from .views import (
    profile_test_view,
    UserProfileData,
    UserProfileView,
)

app_name = 'profiles'

urlpatterns = [
    path('test/', profile_test_view, name='profile-test'),
    path('user/', UserProfileView.as_view(), name='user-profile-json'),
    path('user-json/', UserProfileData.as_view(), name='user-profile-view'),
]
