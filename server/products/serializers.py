from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

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


class ProductsSearchParamsSerializer(serializers.Serializer):
    brand = serializers.CharField(default="")
    type = serializers.CharField(default="")
    sort = serializers.CharField(default="")
    page = serializers.IntegerField(default=1, min_value=1)
    pageSize = serializers.IntegerField(default=6, min_value=1, max_value=50)


class CustomPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "pageSize"
    page_size = 6