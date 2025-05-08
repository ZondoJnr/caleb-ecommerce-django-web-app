from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Password reset flow
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Home
    path('', views.home_view, name='home'),

    # Dashboards
    path('dashboard/vendor/', views.vendor_dashboard, name='vendor_dashboard'),
    path('dashboard/buyer/', views.buyer_dashboard, name='buyer_dashboard'),

    # Store Management (Vendor)
    path('store/create/', views.create_store, name='create_store'),
    path('store/<int:store_id>/edit/', views.edit_store, name='edit_store'),
    path('store/<int:store_id>/delete/', views.delete_store, name='delete_store'),
    path('stores/', views.store_list, name='store_list'),
    path('stores/<int:store_id>/', views.store_detail, name='store_detail'),

    # Product Management (Vendor)
    path('store/<int:store_id>/products/', views.manage_products, name='manage_products'),
    path('store/<int:store_id>/products/add/', views.add_product, name='add_product'),
    path('store/<int:store_id>/products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('store/<int:store_id>/products/delete/<int:product_id>/', views.delete_product, name='delete_product'),

    # Product Management (Dashboard shortcut)
    path('dashboard/vendor/products/', views.vendor_products, name='vendor_products'),
    path('dashboard/vendor/products/add/', views.add_product, name='add_product'),
    path('dashboard/vendor/products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('dashboard/vendor/products/delete/<int:product_id>/', views.delete_product, name='delete_product'),

    # Product Detail and Reviews
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/review/', views.submit_review, name='submit_review'),

    # Cart and Checkout
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),

    # API
    path('api/docs/', TemplateView.as_view(template_name='shop/api_docs.html'), name='api-docs'),
]
