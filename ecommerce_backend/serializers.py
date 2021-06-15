from rest_framework import serializers
from .models import User, Category, Product, Address, OrderItem, Order
from ecommerce_accounts_app.serializers import UserCRUDSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategorySerializerOnlyName(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']

class ProductSerializerOnlyName(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title']

class ProductSerializerNoDesciption(serializers.ModelSerializer):

    image = serializers.ImageField(use_url=True)
    pk = serializers.IntegerField(min_value=0, max_value=None)
    category = CategorySerializerOnlyName(read_only=True)

    class Meta:
        model = Product
        exclude = ['description']

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        exclude = ['user']


class ProductSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(use_url=True)
    pk = serializers.IntegerField(min_value=0, max_value=None)
    category = CategorySerializerOnlyName(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):

    product=ProductSerializer(read_only=True)
    user=UserCRUDSerializer(read_only=True)

    class Meta:
        model=OrderItem
        fields='__all__'

class OrderSerializerItemsOnly(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True,read_only=True)

    class Meta:
        model = Order
        fields = ['items']


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True,read_only=True)

    class Meta:
        model = Order
        fields = ['items']
