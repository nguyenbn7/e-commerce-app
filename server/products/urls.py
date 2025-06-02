from django.urls import path

from products.views import ProductDetail, ProductList

urlpatterns = [
    path("", ProductList.as_view()),
    path("<int:id>", ProductDetail.as_view()),
]
