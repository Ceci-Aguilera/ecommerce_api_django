from django.contrib import admin
from django.conf.urls import url,include
from .views import SignUpAPIView

app_name = 'ecommerce_accounts_app'

urlpatterns = [
    url(r'^sign-up$', SignUpAPIView, name='sign-up-api'),
]
