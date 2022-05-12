from django.urls import path
from .views import (
    profile_test_view,
    received_requests_view,
    profiles_list_view, 
    invite_profiles_list_view, 
    ProfileListView,
    ProfileDetailView, 
    send_requests, 
    remove_from_friends,
    accept_requests,
    reject_requests,
    add_products
)

app_name = 'profiles'

urlpatterns = [
    # path('', ProfileListView.as_view(), name='all-profiles-view'),
    path('profile/', profile_test_view, name='profile-test'),
    path('received-requests/', received_requests_view, name='received-requests'),
    path('all-profiles/', ProfileListView.as_view(), name='all-profiles-view'),
    path('add_products/', add_products, name='add-products'),
    
    path('<slug:slug>', ProfileDetailView.as_view(), name='profile-detail-view'),
    path('to-request/', invite_profiles_list_view, name='request-profiles-view'),
    path('send-requests/',send_requests, name='send-request'),
    path('remove-friend/',remove_from_friends, name='remove-friend'),
    path('received-requests/accept/', accept_requests, name='accept-request'),
    path('received-requests/reject/', reject_requests, name='reject-request'),  
    
]