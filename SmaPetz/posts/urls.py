from django.urls import path
from .views import home_view, PostDeleteView, PostUpdateView, like_unlike_post

app_name = 'posts'

urlpatterns = [
    path('', home_view, name='home-view'),
    path('liked/',like_unlike_post, name='like-post-view'),
    path('<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<pk>/update/', PostUpdateView.as_view(), name='post-update')
]
