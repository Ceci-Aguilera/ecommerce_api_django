
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework import permissions
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status

import json
from knox.models import AuthToken

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib import auth

from .models import User
from .serializers import (
    UserRegisterSerializer,
    UserCRUDSerializer,
    LoginSerializer
)

from ecommerce_backend.models import Address
from ecommerce_backend.serializers import AddressSerializer

# Create your views here.




class CheckAuthenticatedView(RetrieveAPIView):

    permission_classes = [permissions.IsAuthenticated,]

    serializer_class = UserCRUDSerializer

    def get_object(self):
        return self.request.user




class LoginView(GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request, format=None):

        data = request.data
        email = data['email']
        password = data['password']
        result = dict()
        result['flag'] = 'Error Authenticating'
        status_result = status.HTTP_400_BAD_REQUEST

        try:
            user_serializer = self.get_serializer(data=data)

            if user_serializer.is_valid() == False:
                result['flag'] = user_serializer.errors
                status_result = status.HTTP_400_BAD_REQUEST
            else:
                user = user_serializer.validated_data
                result['flag'] = "User Logged In"
                result['user'] = UserCRUDSerializer(
                    user,
                    context=self.get_serializer_context()).data
                result['token'] = AuthToken.objects.create(user)[1]
        except:
            pass

        return Response({'Register result': result}, status=status_result)






class SignUpAPIView(GenericAPIView):

    serializer_class = UserRegisterSerializer

    def post(self, request,*args, **kwargs):

        data = request.data
        password = data['password']
        re_password = data['re_password']
        result = dict()
        result['flag'] = 'User created'
        status_result = status.HTTP_201_CREATED

        if password != re_password:
            result['flag'] = 'Passwords do not match'
            status_result = status.HTTP_400_BAD_REQUEST

        else:
            user_serializer = self.get_serializer(data=data)

            if user_serializer.is_valid() == False:
                result['flag'] = user_serializer.errors
                status_result = status.HTTP_400_BAD_REQUEST
            else:
                user = user_serializer.save()
                result['user'] = UserCRUDSerializer(
                    user,
                    context=self.get_serializer_context()).data
                result['token'] = AuthToken.objects.create(user)[1]

        return Response({'Register result': result}, status=status_result)




class UserManageAccountView(APIView):

    permission_classes = [permissions.IsAuthenticated,]

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

                billing_addresses = AddressSerializer(billing_addresses, many=True).data

                shipping_addresses = AddressSerializer(shipping_addresses, many=True).data

                return Response({'User Account Info':{
                    'User':user,
                    'Billing Addresses': billing_addresses,
                    'Shipping Addresses': shipping_addresses
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
