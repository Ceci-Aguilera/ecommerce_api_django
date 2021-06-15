from django.contrib import admin
from django.conf.urls import url,include
from .views import (
    SignUpAPIView,
    CheckAuthenticatedView,
    LoginView,
    UserManageAccountView,
)

from knox import views as knox_views

app_name = 'ecommerce_accounts_app'

urlpatterns = [
    url(r'^sign-up$', SignUpAPIView.as_view(), name='sign-up-api'),
    url(r'^check-auth/$', CheckAuthenticatedView.as_view(), name='check-auth-api'),
    url(r'^login$', LoginView.as_view(), name='login-api'),
    url(r'^logout$', knox_views.LogoutView.as_view(), name='knox-logout-api'),
    url(r'^manage-account/(?P<pk>[0-9]+)/$', UserManageAccountView.as_view(), name='manage-account-api'),
]
