from rest_framework import generics, permissions
from shop.models import Store, Product, Review
from .serializers import StoreSerializer, ProductSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from utils.twitter import post_tweet

# Create Store
class StoreCreateAPIView(generics.CreateAPIView):
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        store = serializer.save(vendor=self.request.user)
    ''' message = f"🏪 New Store Added!\nName: {store.name}\n{store.description}"
        if store.image:
            post_tweet(message, store.image.path)
        else:
            post_tweet(message)'''

# Add Product
class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product = serializer.save()
'''     message = (
            f"🛍️ New Product in {product.store.name}!\n"
            f"Name: {product.name}\n"
            f"{product.description}"
        )
        if product.image:
            post_tweet(message, product.image.path)
        else:
            post_tweet(message)'''

# List Reviews
class ReviewListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()

# List All Stores 
class StoreListAPIView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

# List Products by Store
class StoreProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        store_name = self.kwargs['store_name']
        store = get_object_or_404(Store, name__iexact=store_name)  # case-insensitive match
        return Product.objects.filter(store=store)