from rest_framework import serializers

from ecommerce_backend.models import Product, Category
from ecommerce_backend.serializers import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(use_url=True)
    pk = serializers.IntegerField(min_value=0, max_value=None)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class ProductMostSellSerializer(serializers.ModelSerializer):

    class Meta:
        models = Product
        fields = ('title', 'amount_sold', 'id')
