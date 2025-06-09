from rest_framework import serializers

from products.models import Product


class ProductViewSerializer(serializers.ModelSerializer):
    pictureUrl = serializers.CharField(source="picture_url")
    quantityInStock = serializers.IntegerField(source="quantity_in_stock")

    class Meta:
        model = Product
        exclude = ("picture_url", "quantity_in_stock", "created_at")


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False)
    price = serializers.IntegerField(min_value=1)
    pictureUrl = serializers.CharField(max_length=255, source="picture_url")
    type = serializers.CharField(max_length=255)
    brand = serializers.CharField(max_length=255)
    quantityInStock = serializers.IntegerField(min_value=0, source="quantity_in_stock")
