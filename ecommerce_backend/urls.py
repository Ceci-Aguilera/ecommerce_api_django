from django.contrib import admin
from django.conf.urls import url,include

from .views import(
    AllProductsView,
    ProductsFromCategory,
    ProductDetail,
    AllCategoriesView,
)

app_name = 'ecommerce_backend'

urlpatterns = [
    url(r'^products$', AllProductsView.as_view(), name='products-api'),
    url(r'^product-detail/(?P<pk>[0-9]+)/$', ProductDetail.as_view(), name='product-detail-api'),
    url(r'^category/products/(?P<pk>[0-9]+)/$', ProductsFromCategory.as_view(), name='category-products-api'),
    url(r'^categories$', AllCategoriesView.as_view(), name='categories-api'),
]
