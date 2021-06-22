from django.contrib import admin
from django.conf.urls import url,include
from .views import (
    SignUpAPIView,
    CheckAuthenticatedView,
    LoginView,
    UserManageAccountView,
    UserManageAddressView,
    CreateAddress,
    ResetPasswordMessage,
    ResetPassword,
    ActivateAccount,
)

from knox import views as knox_views

app_name = 'ecommerce_accounts_app'

urlpatterns = [
    url(r'^sign-up$', SignUpAPIView.as_view(), name='sign-up-api'),
    url(r'^check-auth/$', CheckAuthenticatedView.as_view(), name='check-auth-api'),
    url(r'^login$', LoginView.as_view(), name='login-api'),
    url(r'^logout$', knox_views.LogoutView.as_view(), name='knox-logout-api'),
    url(r'^manage-account/$', UserManageAccountView.as_view(), name='manage-account-api'),
    url(r'^manage-address/(?P<id>[0-9]+)/$', UserManageAddressView.as_view(), name='manage-address-api'),
    url(r'^manage-address/create/$', CreateAddress.as_view(), name='create-address-api'),
    url(r'^reset-password/$', ResetPasswordMessage.as_view(), name='reset-password-message-api'),
    url(r'^reset-password/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', ResetPassword.as_view(), name='reset-password-api'),
    url(r'^activate-account/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', ActivateAccount.as_view(), name='activate-account-api'),

]
