from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import models

from ecommerce_backend.models import *
from ecommerce_accounts_app.models import *
from ecommerce_backend.serializers import *
from ecommerce_accounts_app.serializers import *
from .serializers import ProductSerializer, ProductMostSellSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.generics import (
    GenericAPIView,
    RetrieveAPIView,
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView
    )

from datetime import date, timedelta

# Create your views here.

# ==============================================================================
# User
# ==============================================================================
class UserListView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserCRUDSerializer


class UserManageView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = UserCRUDSerializer
    lookup_field = 'id'

# ==============================================================================
# Order
# ==============================================================================
class OrderListView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderManageView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = OrderSerializer
    lookup_field = 'id'

# ==============================================================================
# Product
# ==============================================================================
class ProductListView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProuductManageView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = ProductSerializer
    lookup_field = 'id'

class ProductMostSell(ListAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = Product.objects.all().order_by('amount_sold')[:10]
    serializer_class = ProductMostSellSerializer

# ==============================================================================
# Refund
# ==============================================================================
class RefundListView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = Refund.objects.all()
    serializer_class = RefundSerializer

class RefundtManageView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = RefundSerializer
    lookup_field = 'id'

# ==============================================================================
# Payment
# ==============================================================================
class PaymentListViewCurrentYear(ListAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = Payment.objects.all().filter(timestamp__year = date.today().year)
    serializer_class = PaymentSerializer


class PaymentListViewCurrentMonth(ListAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = Payment.objects.all().filter(timestamp__month = date.today().month)
    serializer_class = PaymentSerializer

class PaymentListViewCurrentWeek(ListAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_queryset(self):
        current_day = date.today()
        start_week = current_day - timedelta(current_day.weekday())
        end_week = start_week + timedelta(7)
        return Payment.objects.all().filter(timestamp__range = [start_week, end_week])

    serializer_class = PaymentSerializer

class PaymentProportionToUser(GenericAPIView):

    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    def get(self, request, format=None):

        logged_payments = Payment.objects.filter(user__isnull=False).count()
        anonymous_payments = Payment.objects.filter(user__isnull=True).count()

        return Response({"Logged payments": logged_payments, "Anonymous payments": anonymous_payments},
            status=status.HTTP_200_OK,
            )
