from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from django.http import HttpResponse, JsonResponse
import json
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth

from .models import User
from .serializers import UserRegisterSerializer

# Create your views here.


@permission_classes([AllowAny])
class GetCSRFToken(APIView):

    @method_decorator(ensure_csrf_cookie)
    def get(self, request,*args, **kwargs):
        return Response({'Success': 'CSRF cookie set'})



class CheckAuthenticatedView(APIView):

    @method_decorator(csrf_protect)
    def get(self, request, format=None):
        result = 'Success'
        try:
            isAuthenticated = User.is_authenticated
            if isAuthenticated == False:
                result='Error'
        except:
            result = 'Error'

        return Response({'isAuthenticated':result})




@permission_classes([AllowAny])
class LoginView(APIView):

    @method_decorator(csrf_protect)
    def post(self, request, format=None):

        data = request.data
        email = data['email']
        password = data['password']
        result = 'Error Authenticating'
        try:
            user = auth.authenticate(username=email,password=password)
            if user is not None:
                auth.login(request, user)
                result = 'Success at Authenticating'
        except:
            pass

        return Response({'Login Result':result})



class LogoutView(APIView):

    def post(self, request, format=None):
        try:
            auth.logout(request)
            result = 'Success'
        except:
            result = 'Something went wrong when logging out'
        return Response({'Logout Result':result})



@permission_classes([AllowAny])
class SignUpAPIView(APIView):

    @method_decorator(csrf_protect)
    def post(self, request,*args, **kwargs):

        data = request.data
        password = data['password']
        re_password = data['re_password']
        result = 'User created'
        status_result = status.HTTP_201_CREATED

        if password != re_password:
            result = 'Passwords do not match'
            status_result = status.HTTP_400_BAD_REQUEST

        else:
            user_serializer = UserRegisterSerializer(data=data)

            if user_serializer.is_valid() == False:
                result = user_serializer.errors
                status_result = status.HTTP_400_BAD_REQUEST
            else:
                user = user_serializer.save()

        return Response({'Register result': result}, status=status_result)
