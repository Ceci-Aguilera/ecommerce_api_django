from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView

import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.mail import send_mail

from .models import Product, Order, OrderItem, Category, Address
from .serializers import(
    ProductSerializerNoDesciption,
    ProductSerializer,
    CategorySerializer,
    OrderItemSerializer,
    OrderSerializerItemsOnly,
    OrderSerializer,
    AddressSerializer,
)


# Create your views here.

#====================================================
def add_to_cart(request, productItem):
    try:
        user = request.user
        if user is not None:
            order, created = Order.objects.get_or_create(
                user = user,
                ordered = False
            )
            #Check if item was already added before
            for eachProduct in order.items.all():
                if eachProduct.product == productItem.product:
                    quantity = eachProduct.quantity + productItem.quantity
                    productItem.quantity = max(0, quantity)
                    productItem.save()
                    eachProduct.order_set.remove()
                    eachProduct.delete()
                    break

            order.items.add(productItem)
            result = order.pk

    # Anonymous User
    except:
        order_pk = request.data['order_pk']
        try:
            order = Order.objects.get(
                pk = order_pk,
                ordered = False,
                user = None
            )
        except:
            try:
                order = Order.objects.create()
                order_pk = order.pk
            except:
                result='Error'
                return result
        for eachProduct in order.items.all():
            if eachProduct.product == productItem.product:
                quantity = eachProduct.quantity + productItem.quantity
                productItem.quantity = max(0, quantity)
                productItem.save()
                eachProduct.order_set.remove()
                eachProduct.delete()
                break

        order.items.add(productItem)
        result = order_pk

    return result;



#======================================================

class AllProductsView(APIView):

    def get(self, request, format=None):

        try:
            search_params = request.query_params.get('search_keyword')
            products = Product.objects.filter(title__icontains=search_params).defer('description')
        except:
            products = Product.objects.all()

        serializer = ProductSerializerNoDesciption(products, many=True, context={'request': request})
        productsToJson = serializer.data
        return Response(productsToJson, status=status.HTTP_201_CREATED)








class AllCategoriesView(ListAPIView):

    serializer_class = CategorySerializer
    model = Category
    queryset = Category.objects.all()








class ProductsFromCategory(APIView):

    def get(self, request, id, *args, **kwargs):

        try:
            search_params = request.query_params.get('search_keyword')
            products = Product.objects.filter(category__id=id, title__icontains=search_params).defer('description')
        except:
            products = Product.objects.filter(category__id=id).defer('description')

        serializer = ProductSerializerNoDesciption(products, many=True, context={'request': request})
        productsToJson = serializer.data
        return Response(productsToJson, status=status.HTTP_201_CREATED)







class ProductDetail(APIView):

    def get(self, request, pk, *args, **kwargs):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, context={'request': request})
        productToJson = serializer.data
        return Response(productToJson, status=status.HTTP_201_CREATED)


    def post(self, request, pk, *args, **kwargs):
        product = Product.objects.get(pk=pk)
        serializer = OrderItemSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        try:
            orderItem = serializer.save(user=request.user, product=product)
            result = add_to_cart(request=request, productItem=orderItem)
            status_result = status.HTTP_200_OK
            return Response({"Add to cart result": result}, status=status_result)
        except:
            orderItem = serializer.save(user=None, product=product)
            result = add_to_cart(request=request, productItem=orderItem)
            status_result = status.HTTP_200_OK
            return Response({"Add to cart result": result}, status=status_result)







class CartView(APIView):

    def get(self, request, format=None):
        try:
            pk = self.request.user.pk
            order = Order.objects.get(
                user__pk = pk,
                ordered=False
            )
        # Manage Anonymous User
        except:
            try:
                order_pk = request.query_params.get('order_pk')
                order = Order.objects.get(pk=order_pk)
                if order.ordered == True or order.user != None:
                    return Response({}, status=status.HTTP_201_CREATED)
            except:
                return Response({}, status=status.HTTP_201_CREATED)

        serializer = OrderSerializerItemsOnly(order, context={'request': request})
        orderToJson = serializer.data
        return Response(orderToJson, status=status.HTTP_201_CREATED)


    def post(self, request,*args, **kwargs):
        try:
            pk = self.request.user.pk
            order = Order.objects.all().get(
                user__pk = pk,
                ordered=False
            )
        except:
            order_pk = request.data['order_pk']
            order = Order.objects.get(pk=order_pk)

        item_to_delete = request.data["item_to_delete"]
        product_pk = item_to_delete['product']['pk']
        product = Product.objects.get(pk=product_pk)
        item_to_delete = OrderItemSerializer(data=item_to_delete, context={'request':request})
        if item_to_delete.is_valid(raise_exception=True):


            user = None if request.user.is_anonymous else request.user

            item_to_delete = item_to_delete.save(user=user, product=product)

            for item in order.items.all():
                if item.product == item_to_delete.product:
                    item.order_set.remove()
                    item.delete()
            return Response(
                {"Delete Item from cart":"Success"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"Delete Item from cart":"Error"},
            status=status.HTTP_400_BAD_REQUEST,
        )


    def delete(self, request, *args, **kwargs):

        try:
            pk = self.request.user.pk
            order = Order.objects.all().get(
                user__pk = pk,
                ordered=False
                )
        except:
            order_pk = request.query_params.get('order_pk')
            order = Order.objects.get(pk=order_pk)

        try:
            items = order.items.all()
            for item in items:
                item.order_set.remove()
                item.delete()
            order.delete()
            return Response(
                {"Delete cart":"Success"},
                status=status.HTTP_201_CREATED
            )
        except:
            return Response(
                {"Delete cart":"Error"},
                status=status.HTTP_400_BAD_REQUEST
            )







class Checkout(GenericAPIView):

    serializer_class = OrderSerializer

    def get(self, request, pk, format=None):

        order = Order.objects.get(pk=pk)

        if order.billing_address == None:
            try:
                billing_address = Address.objects.get(user=request.user, address_type="B", default=True)
                order.billing_address = billing_address
            except:
                pass
        if order.shipping_address == None:
            try:
                shipping_address = Address.objects.get(user=request.user, address_type="S", default=True)
                order.shipping_address = shipping_address
            except:
                pass

        order.save()
        order_serializer = self.get_serializer(order)

        return Response({"Order Summary": order_serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk, forma=None):

        # try:
        if(True):
            order = Order.objects.get(pk=pk)
            if order.user is not None:
                if order.user != request.user:
                    return Response({"Order Summary": "Error while updating"}, status=status.HTTP_400_BAD_REQUEST)
            # BILLING AND SHIPPING ADDRESSES
            try:
                billing_address_id = request.data['billing_address']['id']
                order.billing_address = Address.objects.get(id = billing_address_id)
                order.save()
            except:
                pass

            try:
                shipping_address_id = request.data['shipping_address']['id']
                order.shipping_address = Address.objects.get(id = shipping_address_id)
                order.save()
            except:
                pass

            order_serializer = self.get_serializer(order)
            return Response({"Order Summary": order_serializer.data}, status=status.HTTP_200_OK)


        # except:
        else:
            return Response({"Order Summary": "Error while updating"}, status=status.HTTP_400_BAD_REQUEST)







class AllAddressesView(GenericAPIView):

    serializer_class = AddressSerializer

    def get(self, request, format=None):

        billing_addresses = Address.objects.all().filter(user = request.user, address_type="B")
        shipping_addresses = Address.objects.all().filter(user = request.user, address_type="S")

        billing_addresses_serializer = self.get_serializer(billing_addresses, many=True)
        billing_addresses = billing_addresses_serializer.data

        shipping_addresses_serializer = self.get_serializer(shipping_addresses, many=True)
        shipping_addresses = shipping_addresses_serializer.data
        return Response({"Billing_addresses": billing_addresses, "Shipping_addresses":shipping_addresses}, status=status.HTTP_200_OK)







class OrderRetrieve(RetrieveAPIView):

    serializer_class = OrderSerializer

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        order = Order.objects.get(pk=pk)
        if order.user is not None:
            if order.user != self.request.user:
                return None
        return order
