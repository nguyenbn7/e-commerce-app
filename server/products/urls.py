from django.urls import path

from products.views import ProductBrandList, ProductDetail, ProductList, ProductTypeList

urlpatterns = [
    path("", ProductList.as_view()),
    path("<int:id>", ProductDetail.as_view()),
    path("brands", ProductBrandList.as_view()),
    path("types", ProductTypeList.as_view()),
]
