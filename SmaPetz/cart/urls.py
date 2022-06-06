from django.urls import path
from .views import cart_detail, success

app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart'),
    path('success/', success, name='success')
]
