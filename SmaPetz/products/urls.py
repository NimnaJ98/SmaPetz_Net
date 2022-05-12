from django.urls import path
from .views import store_view, product, category, searchProduct

app_name = 'products'

urlpatterns = [
    path('store/', store_view, name='store-view'),
    path('search/', searchProduct, name='product-search'),
    path('<slug:category_slug>/<slug:product_slug>/', product, name='product'),
    path('<slug:category_slug>/', category, name='category'),
]