from django.http import HttpRequest
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException, NotFound

from products.models import Product
from products.serializers import (
    GetProductsResponseSerializer,
    GetProductResponseSerializer,
)

# Create your views here.


class ProductList(APIView):
    def get(self, request: HttpRequest, format=None):
        products = Product.objects.all()

        response_serializer = GetProductsResponseSerializer(products, many=True)

        return Response({"products": response_serializer.data})


class ProductDetail(APIView):
    def get(self, request: HttpRequest, id, format=None):
        product = Product.objects.filter(pk=id).first()

        if not product:
            raise NotFound("Product not found", code="not_found")

        response_serializer = GetProductResponseSerializer(product)

        return Response({"product": response_serializer.data})
