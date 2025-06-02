from rest_framework import serializers

from products.models import Product


class GetProductsResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class GetProductResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
