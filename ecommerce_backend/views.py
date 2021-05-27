from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.conf import settings
from django.core.mail import send_mail
# from django.middleware.csrf import get_token

from .models import Product
from .serializers import ProductSerializerNoDesciption

# def get_csrf(request):
#     if request.method == 'GET':
#         response = JsonResponse({'Info':'Success - Set CSRF cookie'})
#         response['X-CSRFToken'] = get_token(request)
#         return response

# Create your views here.
@api_view(['GET'])
def HomeViewAPI(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializerNoDesciption(products, many=True, context={'request': request})
        productsToJson = serializer.data
        return Response(productsToJson, status=status.HTTP_201_CREATED)
