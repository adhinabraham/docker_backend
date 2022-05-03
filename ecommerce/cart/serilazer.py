
from itertools import product
from rest_framework import serializers
from .models import Cart
from products.serilazer import MyproductSerializer
from users.serializer import  MyUser

class MycartShowSerializer(serializers.ModelSerializer):
    username=MyUser()
    products = serializers.CharField(source='product_id.productname')  
    image_url = serializers.ImageField(source='product_id.image')
    price=serializers.CharField(source='product_id.price')
    sub_total=serializers.CharField
    # photo_url = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)


    class Meta:
        model = Cart
        fields = ['username','id','product_id','products','product_stock','price','sub_total','image_url']


class CartSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Cart
        fields = '__all__'

   


