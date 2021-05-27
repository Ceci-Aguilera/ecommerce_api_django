from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from django.http import HttpResponse, JsonResponse
import json
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserRegisterSerializer

# Create your views here.

# @method_decorator(ensure_csrf_cookie, name='dispatch')
@api_view(['GET',])
@ensure_csrf_cookie
@permission_classes([AllowAny])
def GetCSRFToken(request):
    permissions_classes = [AllowAny, ]

    if request.method == 'GET':
        return Response({'success': 'CSRF cookie set'})


@api_view(['POST',])
@permission_classes([AllowAny])
@csrf_protect
def SignUpAPIView(request):
    permissions_classes = [AllowAny, ]

    if request.method=='POST':

        # return Response("OK")

        data = request.data
        password = data['password']
        re_password = data['re_password']

        if password != re_password:
            return Response(
                {'error':'Password does not match'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_serializer = UserRegisterSerializer(data=data)
        if user_serializer.is_valid() == False:
            return Response(
                {'error': user_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = user_serializer.save()
        return Response(
            {'status': 'User created'},
            status=status.HTTP_201_CREATED
        )
