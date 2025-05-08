from rest_framework import serializers
from shop.models import Store, Product, Review
from django.core.exceptions import ObjectDoesNotExist


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'description', 'image', 'created_at', 'vendor']
        read_only_fields = ['vendor']  

class ProductSerializer(serializers.ModelSerializer):
    store = serializers.CharField(required=True)  # Accept store name as input

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'image', 'store']

    def validate_store(self, value):
        user = self.context['request'].user
        try:
            # Try to find the store by name that belongs to this vendor
            store = Store.objects.get(name=value, vendor=user)
        except Store.DoesNotExist:
            raise serializers.ValidationError("Store with this name does not exist or is not owned by you.")
        return store  # Return the Store instance

    def create(self, validated_data):
        # Replace 'store' string with actual Store object
        store = validated_data.pop('store')
        product = Product.objects.create(store=store, **validated_data)
        return product

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'created_at', 'is_verified']
