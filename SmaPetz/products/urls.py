from django.urls import path
from .views import store_view

app_name = 'products'

urlpatterns = [
    path('store/', store_view, name='store-view'),
]