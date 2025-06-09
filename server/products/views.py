from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotFound

from products.models import Product
from products.serializers import (
    ProductSerializer,
    ProductViewSerializer,
)

# Create your views here.


class ProductList(APIView):
    def get(self, request: Request, format=None):
        brand_query_str = request.query_params.get("brand", "")
        type_query_str = request.query_params.get("type", "")
        sort_query_str = request.query_params.get("sort", "")

        query = Product.objects

        if brand_query_str:
            query = query.filter(brand__exact=brand_query_str)

        if type_query_str:
            query = query.filter(type__exact=type_query_str)

        match sort_query_str:
            case "price":
                query = query.order_by("price")
            case "-price":
                query = query.order_by("-price")
            case _:
                query = query.order_by("name")

        products = query.all()

        response_serializer = ProductViewSerializer(products, many=True)

        return Response({"products": response_serializer.data})

    def post(self, request: Request, format=None):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        create_product_data = serializer.validated_data

        new_product = Product(**create_product_data)
        new_product.save()

        response_serializer = ProductViewSerializer(new_product)

        return Response({"product": response_serializer.data})


class ProductDetail(APIView):
    def get(self, request: Request, id, format=None):
        product = Product.objects.filter(pk=id).first()

        if not product:
            raise NotFound("Product not found", code="not_found")

        response_serializer = ProductViewSerializer(product)

        return Response({"product": response_serializer.data})

    def put(self, request: Request, id, format=None):
        product = Product.objects.filter(pk=id).first()

        if not product:
            raise NotFound("Product not found", code="not_found")

        serializer = ProductSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        Product.objects.filter(pk=id).update(**serializer.validated_data)

        product.refresh_from_db()

        response_serializer = ProductViewSerializer(product)

        return Response({"product": response_serializer.data})


class ProductBrandList(APIView):
    def get(self, request: Request, format=None):
        brands = Product.objects.values_list("brand", flat=True).distinct()

        return Response({"brands": brands})


class ProductTypeList(APIView):
    def get(self, request: Request, format=None):
        types = Product.objects.values_list("type", flat=True).distinct()

        return Response({"types": types})
