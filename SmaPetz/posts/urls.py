from django.urls import path
from .views import home_view, PostDeleteView, PostUpdateView

app_name = 'posts'

urlpatterns = [
    path('', home_view, name='home-view'),
    path('<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<pk>/update/', PostUpdateView.as_view(), name='post-update')
]
