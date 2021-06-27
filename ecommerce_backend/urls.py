from django.contrib import admin
from django.conf.urls import url,include

from .views import(
    AllProductsView,
    ProductsFromCategory,
    ProductDetail,
    AllCategoriesView,
    CartView,
    Checkout,
    AllAddressesView,
    OrderRetrieve,
    PaymentView,
    AllOrders,
)

app_name = 'ecommerce_backend'

urlpatterns = [
    url(r'^products$', AllProductsView.as_view(), name='products-api'),
    url(r'^product-detail/(?P<pk>[0-9]+)/$', ProductDetail.as_view(), name='product-detail-api'),
    url(r'^category/products/(?P<id>[0-9]+)/$', ProductsFromCategory.as_view(), name='category-products-api'),
    url(r'^categories$', AllCategoriesView.as_view(), name='categories-api'),
    url(r'^cart$', CartView.as_view(), name='cart-api'),
    url(r'^checkout/(?P<pk>[0-9]+)/$', Checkout.as_view(), name='checkout-view'),
    url(r'^account-addresses$', AllAddressesView.as_view(), name='addresses-view'),
    url(r'^account-order/(?P<pk>[0-9]+)/$', OrderRetrieve.as_view(), name='order-view'),
    url(r'^payment/(?P<pk>[0-9]+)/$', PaymentView.as_view(), name='payment-view'),
    url(r'^user-orders/$', AllOrders.as_view(), name='user-orders-view'),
]
