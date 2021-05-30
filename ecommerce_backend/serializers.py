from rest_framework import serializers
from .models import User, Category, Product, Address

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategorySerializerOnlyName(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']

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
