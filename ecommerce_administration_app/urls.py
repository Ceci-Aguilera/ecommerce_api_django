from django.contrib import admin
from django.conf.urls import url,include

from .views import(
    UserListView,
    UserManageView,
    OrderListView,
    OrderManageView,
    ProductListView,
    ProuductManageView,
    ProductMostSell,
    RefundListView,
    RefundtManageView,
    PaymentListViewCurrentYear,
    PaymentListViewCurrentMonth,
    PaymentListViewCurrentWeek,
    PaymentProportionToUser,
)

app_name = 'ecommerce_administration_app'

urlpatterns = [
    url(r'^user-list$', UserListView.as_view(), name='user-list-api'),
    url(r'^user-manage/(?P<id>[0-9]+)/$', UserManageView.as_view(), name='user-manage-api'),
    url(r'^order-list$', OrderListView.as_view(), name='order-list-api'),
    url(r'^order-manage/(?P<pk>[0-9]+)/$', OrderManageView.as_view(), name='order-manage-api'),
    url(r'^product-list$', ProductListView.as_view(), name='product-list-api'),
    url(r'^product-manage/(?P<pk>[0-9]+)/$', ProuductManageView.as_view(), name='product-manage-api'),
    url(r'^products-most-sell$', ProductMostSell.as_view(), name='products-most-sell-api'),
    url(r'^refund-list$', RefundListView.as_view(), name='refund-list-api'),
    url(r'^refund-manage/(?P<pk>[0-9]+)/$', RefundtManageView.as_view(), name='refund-manage-api'),
    url(r'^payment-year-list$', PaymentListViewCurrentYear.as_view(), name='payment-year-list-api'),
    url(r'^payment-month-list$', PaymentListViewCurrentMonth.as_view(), name='payment-month-list-api'),
    url(r'^payment-week-list$', PaymentListViewCurrentWeek.as_view(), name='payment-week-list-api'),
    url(r'^payment-proportion-user$', PaymentProportionToUser.as_view(), name='payment-proportion-user-api'),
]
