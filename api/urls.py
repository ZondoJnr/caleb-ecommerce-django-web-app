from django.urls import path
from . import views

urlpatterns = [
    path('stores/', views.StoreListAPIView.as_view(), name='store-list'),
    path('stores/create/', views.StoreCreateAPIView.as_view(), name='store-create'),
    path('products/create/', views.ProductCreateAPIView.as_view(), name='product-create'),
    path('reviews/', views.ReviewListAPIView.as_view(), name='review-list'),
    path('stores/<str:store_name>/products/', views.StoreProductListAPIView.as_view(), name='store-product-list'),  # updated
]
