from django.urls import path
from .views import store_view, product

app_name = 'products'

urlpatterns = [
    path('store/', store_view, name='store-view'),
    path('<slug:category_slug>/<slug:product_slug>/', product, name='product'),
]