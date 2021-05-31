from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.decorators import authentication_classes, permission_classes
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.conf import settings
from django.core.mail import send_mail

from .models import Product
from .serializers import(
    ProductSerializerNoDesciption,
    ProductSerializer,
    CategorySerializer,
)


# Create your views here.

@permission_classes([AllowAny])
class AllProductsView(APIView):

    @method_decorator(csrf_protect)
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializerNoDesciption(products, many=True, context={'request': request})
        productsToJson = serializer.data
        return Response(productsToJson, status=status.HTTP_201_CREATED)



@permission_classes([AllowAny])
class ProductsFromCategory(APIView):

    @method_decorator(csrf_protect)
    def get(self, request, pk, *args, **kwargs):
        products = Product.objects.filter(category__pk=pk).defer('description')
        serializer = ProductSerializerNoDesciption(products, many=True, context={'request': request})
        productsToJson = serializer.data
        return Response(productsToJson, status=status.HTTP_201_CREATED)



@permission_classes([AllowAny])
class ProductDetail(APIView):

    @method_decorator(csrf_protect)
    def get(self, request, pk, *args, **kwargs):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, context={'request': request})
        productToJson = serializer.data
        return Response(productToJson, status=status.HTTP_201_CREATED)



@permission_classes([AllowAny])
class AllCategoriesView(APIView):

    @method_decorator(csrf_protect)
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        categoriesToJson = serializer.data
        return Response(categoriesToJson, status=status.HTTP_201_CREATED)
