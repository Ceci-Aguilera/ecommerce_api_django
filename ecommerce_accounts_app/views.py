from rest_framework.views import APIView
from rest_framework.generics import (
    GenericAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView
)
from rest_framework import permissions
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status

import json
from knox.models import AuthToken

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage

from .models import User
from .serializers import (
    UserRegisterSerializer,
    UserCRUDSerializer,
    LoginSerializer
)

from ecommerce_backend.models import Address, Order
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
        result = dict()
        result['flag'] = 'Error Authenticating'
        status_result = status.HTTP_400_BAD_REQUEST

        try:
            user_serializer = self.get_serializer(data=data['user'])

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
                status_result = status.HTTP_201_CREATED
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
                user.is_active = False
                user.save()
                result['user'] = UserCRUDSerializer(
                    user,
                    context=self.get_serializer_context()).data
                result['token'] = AuthToken.objects.create(user)[1]

                #ACTIVATION CODE
                user.last_uid=urlsafe_base64_encode(force_bytes(user.pk))
                user.save()
                user.last_token=default_token_generator.make_token(user)
                user.save()

                # current_site = get_current_site(request)

                email_subject="Activate your account."
                message=render_to_string('ecommerce_accounts_api/activate_account.html', {
                    'user': user.email,
                    # 'domain': current_site.domain,
                    'uid': user.last_uid,
                    'token':user.last_token,
                })
                to_email = user.email
                email = EmailMessage(email_subject, message, to=[to_email])
                email.send()

        return Response({'Register result': result}, status=status_result)






class ActivateAccount(APIView):

    def get(self, request, uid, token, format=None):

        try:
            pk = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(last_uid = uid, last_token = token, pk=pk)
            user.is_active = True
            user.save()
            return Response({"Result": "Success"}, status=status.HTTP_200_OK)
        except:
            return Response({'Result':'Error'}, status=status.HTTP_400_BAD_REQUEST)







class UserManageAccountView(APIView):

    permission_classes = [permissions.IsAuthenticated,]

    def delete(self, request, format=None):

        try:
            user = request.user.delete()
            return Response({'Delete User Result':"Success"},
                status=status.HTTP_201_CREATED)
        except:
            return Response({'Delete User Result':"Error"},
                status=status.HTTP_400_BAD_REQUEST)



    def get(self, request, format=None):

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


    def put(self, request, format=None):

        try:
            user = UserCRUDSerializer(request.user, data=request.data, partial=True)
            user.is_valid(raise_exception=True)
            user.save()
            return Response({'User':user.data},
                    status=status.HTTP_200_OK)
        except:
            return Response({'User':"Error reading User's account"},
                status=status.HTTP_400_BAD_REQUEST)






class UserManageAddressView(RetrieveUpdateDestroyAPIView):

    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    lookup_field = 'id'






class CreateAddress(GenericAPIView):

    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = AddressSerializer

    def post(self, request, format='None'):
        try:
            user = request.user
        except:
            user = None

        data  = request.data
        address_serializer = self.get_serializer(data=data)
        address_serializer.is_valid(raise_exception=True)
        address_serializer.save(user = user)
        return Response({"Address": address_serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, format='None'):
        print(request.data)
        data = request.data
        id = data['id']
        address_type = data['address_type']
        user = request.user

        try:
            old_default = Address.objects.get(default=True, address_type=address_type, user=user)
            old_default.default=False
            old_default.save()
        except:
            pass

        try:
            new_default = Address.objects.get(id=id, user=user)
            new_default.default=True
            new_default.save()
        except:
            return Response({"Set Default Result": "Error"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"Set Default Result": "Error"}, status=status.HTTP_200_OK)




class ResetPasswordMessage(APIView):

    def post(self, request, format=None):
        # current_site = get_current_site(request)
        email_subject = "Reset your password"
        try:
            user = User.objects.get(email=request.data['email'])
            user.last_uid_password=urlsafe_base64_encode(force_bytes(user.pk))
            user.save()
            user.last_token_password=default_token_generator.make_token(user)
            user.save()
            message=render_to_string('ecommerce_accounts_api/reset_password.html', {
                'user': user.email,
                # 'domain': current_site.domain,
                'uid': user.last_uid_password,
                'token': user.last_token_password,
            })
            to_email = user.email
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            request_response='Email sent with a link to change password'
            return Response({"Result": request_response}, status=status.HTTP_200_OK)

        except:
            return Response({"Result": "Error"}, status=status.HTTP_400_BAD_REQUEST)






class ResetPassword(APIView):

    def post(self, request, uid, token, format=None):

        try:
            user = User.objects.get(last_uid_password = uid, last_token_password = token)
            password = request.data['password']
            re_password = request.data['re_password']
            if password != re_password:
                return Response({'Result':'Password does not match'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(password)
            user.save()
            return Response({"Result": "Success"}, status=status.HTTP_200_OK)
        except:
            return Response({'Result':'Error'}, status=status.HTTP_400_BAD_REQUEST)
