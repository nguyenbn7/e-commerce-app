from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotFound

from products.models import Product
from products.serializers import (
    ProductSerializer,
    ProductViewSerializer,
    ProductsSearchParamsSerializer,
    CustomPagination,
)

# Create your views here.


class ProductList(APIView):
    def get(self, request: Request, format=None):
        search_params_serializer = ProductsSearchParamsSerializer(
            data=request.query_params.dict()
        )
        search_params_serializer.is_valid(raise_exception=True)
        search_params = search_params_serializer.validated_data

        query = Product.objects

        if search_params["brand"]:
            query = query.filter(brand__exact=search_params["brand"])

        if search_params["type"]:
            query = query.filter(type__exact=search_params["type"])

        match search_params["sort"].lower():
            case "price":
                query = query.order_by("price")
            case "-price":
                query = query.order_by("-price")
            case _:
                query = query.order_by("name")

        queryset = query.all()

        pagination = CustomPagination()
        pagination.paginate_queryset(queryset=queryset, request=request)

        page_product = pagination.page

        response_serializer = ProductViewSerializer(list(page_product), many=True)

        return Response(
            {
                "links": {
                    "next": pagination.get_next_link(),
                    "prev": pagination.get_previous_link(),
                },
                "previousPage": (
                    page_product.previous_page_number()
                    if page_product.has_previous()
                    else None
                ),
                "nextPage": (
                    page_product.next_page_number() if page_product.has_next() else None
                ),
                "page": page_product.number,
                "pageSize": page_product.paginator.per_page,
                "totalPages": page_product.paginator.num_pages,
                "total": page_product.paginator.count,
                "count": len(response_serializer.data),
                "products": response_serializer.data,
            }
        )

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
