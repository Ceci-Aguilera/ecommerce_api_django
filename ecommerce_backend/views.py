from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework.decorators import authentication_classes, permission_classes

import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.mail import send_mail

from .models import Product, Order, OrderItem
from .serializers import(
    ProductSerializerNoDesciption,
    ProductSerializer,
    CategorySerializer,
    OrderItemSerializer,
    OrderSerializerItemsOnly,
)


# Create your views here.

#====================================================
def add_to_cart(request, productItem):
    try:
        user = request.user
        if user is not None:
            order, created = Order.objects().get_or_create(
                user = request.user,
                ordered = False
            )
            #Check if item was already added before
            if OrderItem.order_set.filter(pk=order.pk).exists():

                product_base = productItem.product
                old_ordered_item = OrderItem.objects.filter(
                    product__title=product_base.title,
                    order__pk = order.pk
                )
                productItem.quantity += product_base.quantity
                product_base.delete()

            order.items.add(productItem)
            result='Success'
        else:
            result='Invalid User'

    except:
            result='Error'
    return result;



#======================================================

class AllProductsView(APIView):

    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializerNoDesciption(products, many=True, context={'request': request})
        productsToJson = serializer.data
        return Response(productsToJson, status=status.HTTP_201_CREATED)




class ProductsFromCategory(APIView):

    def get(self, request, pk, *args, **kwargs):
        products = Product.objects.filter(category__pk=pk).defer('description')
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
            result = add_to_cart(request=request, productItem=ProductItem)
            status_result = status.HTTP_201_CREATED if result=='Success' else status.HTTP_400_BAD_REQUEST
            return Response({"Add to cart result": result}, status=status_result)
        except:
            return Response({"Add to cart result":"Error"}, status=status.HTTP_400_BAD_REQUEST)



class AllCategoriesView(APIView):

    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        categoriesToJson = serializer.data
        return Response(categoriesToJson, status=status.HTTP_201_CREATED)



class CartView(APIView):

    permission_classes = [permissions.IsAuthenticated,]

    def get(self, request, pk, *args, **kwargs):
        order = Order.objects.all().filter(
            user__pk = pk,
            ordered=False
        )
        serializer = OrderSerializerItemsOnly(order, context={'request': request})
        orderToJson = serializer.data
        return Response(orderToJson, status=status.HTTP_201_CREATED)


    def post(self, request, pk, *args, **kwargs):
        order = Order.objects.all().filter(
            user__pk = pk,
            ordered=False
        )
        item_to_delete = request.data["item_to_delete"]
        item_to_delete = OrderItemSerializer(data=item_to_delete, context={'request':request})
        if item_to_delete.is_valid(raise_exception=True):
            item_to_delete.save()
            item_to_delete.delete()
            return Response(
                {"Delete Item from cart":"Success"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"Delete Item from cart":"Error"},
            status=status.HTTP_400_BAD_REQUEST,
        )


    def delete(self, request, pk, *args, **kwargs):
        try:
            order = Order.objects.get(pk=pk)
            items = order.items
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
