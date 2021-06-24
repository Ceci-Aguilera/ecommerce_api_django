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
    total_product_price = serializers.SerializerMethodField('get_total_product_price')
    total_discount_product_price = serializers.SerializerMethodField('get_total_discount_product_price')
    amount_saved = serializers.SerializerMethodField('get_amount_saved')
    final_price = serializers.SerializerMethodField('get_final_price')

    def get_total_product_price(self, obj):
        if obj.product is not None:
            return obj.quantity * obj.product.price
        return 0

    def get_total_discount_product_price(self, obj):
        if obj.product is not None:
            return (obj.quantity * obj.product.price) - (obj.quantity * obj.product.discount_price)
        return 0


    def get_amount_saved(self, obj):
        if obj.product is not None:
            return obj.quantity * obj.product.discount_price
        return 0

    def get_final_price(self, obj):
        if obj.product is not None:
            if obj.product.discount_price:
                return (obj.quantity * obj.product.price) - (obj.quantity * obj.product.discount_price)
            return (obj.quantity * obj.product.price)
        return 0

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
    user = UserCRUDSerializer(read_only=True)
    billing_address = AddressSerializer(read_only=True)
    shipping_address = AddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
