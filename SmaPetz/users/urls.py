from django.urls import path, re_path, reverse_lazy
from .views import register, login_view, logout_view, home_view, about_view,vet_view
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

app_name = 'users'

urlpatterns = [
    path('', home_view, name='dashboard'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('about/', about_view, name='about-view'),    
    path('vet/', vet_view, name='vet-view'), 

]
