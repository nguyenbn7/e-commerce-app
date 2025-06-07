from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from products.models import Product
from products.serializers import (
    ProductSerializer,
    ProductViewSerializer,
)

# Create your views here.


class ProductList(APIView):
    def get(self, request: HttpRequest, format=None):
        products = Product.objects.all()

        response_serializer = ProductViewSerializer(products, many=True)

        return Response({"products": response_serializer.data})

    def post(self, request: HttpRequest, format=None):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        create_product_data = serializer.validated_data

        new_product = Product(**create_product_data)
        new_product.save()

        response_serializer = ProductViewSerializer(new_product)

        return Response({"product": response_serializer.data})


class ProductDetail(APIView):
    def get(self, request: HttpRequest, id, format=None):
        product = Product.objects.filter(pk=id).first()

        if not product:
            raise NotFound("Product not found", code="not_found")

        response_serializer = ProductViewSerializer(product)

        return Response({"product": response_serializer.data})

    def put(self, request: HttpRequest, id, format=None):
        product = Product.objects.filter(pk=id).first()

        if not product:
            raise NotFound("Product not found", code="not_found")

        serializer = ProductSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        Product.objects.filter(pk=id).update(**serializer.validated_data)

        product.refresh_from_db()

        response_serializer = ProductViewSerializer(product)

        return Response({"product": response_serializer.data})
