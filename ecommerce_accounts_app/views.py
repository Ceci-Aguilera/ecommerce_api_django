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
from .serializers import UserRegisterSerializer, UserCRUDSerializer
from ecommerce_backend.models import Address
from ecommerce_backend.serializers import AddressSerializer

# Create your views here.


@permission_classes([AllowAny])
class GetCSRFToken(APIView):

    @method_decorator(ensure_csrf_cookie)
    def get(self, request,*args, **kwargs):
        return Response({'Success': 'CSRF cookie set'})



class CheckAuthenticatedView(APIView):

    @method_decorator(csrf_protect)
    def get(self, request, pk, format=None):
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




class UserManageAccountView(APIView):

    def delete(self, request, pk, format=None):

        try:
            user = request.user.delete()
            return Response({'Delete User Result':"Success"},
                status=status.HTTP_201_CREATED)
        except:
            return Response({'Delete User Result':"Error"},
                status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, pk, format=None):

        try:
            user = request.user
            user = UserCRUDSerializer(user)
            if user.is_valid:
                user = user.data

                billing_addresses = Address.objects.all().filter(
                    user=request.user,
                    address_type='B')
                shipping_addresses = Address.objects.all().filter(
                    user=request.user,
                    address_type='S')


                # if billing_addresses.exists():
                billing_addresses = AddressSerializer(billing_addresses, many=True).data
                # else:
                #     billing_address = 'NULL'

                # if shipping_addresses.exists():
                shipping_addresses = AddressSerializer(shipping_addresses, many=True).data
                # else:
                #     shipping_addresses = 'NULL'

                return Response({'User Account Info':{
                    'User':user,
                    'Billing Addresses': billing_addresses,
                    'Shipping Addresses': shipping_addresses
                    # 'a':'a',
                }},
                    status=status.HTTP_201_CREATED)
        except:
            pass

        return Response({'User':"Error reading User's account"},
            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):

        try:
            user = UserCRUDSerializer(request.user, data=request.data, partial=True)
            user.is_valid(raise_exception=True)
            user.save()
            return Response({'User':user.data},
                    status=status.HTTP_200_OK)
        except:
            return Response({'User':"Error reading User's account"},
                status=status.HTTP_400_BAD_REQUEST)
