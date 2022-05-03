
from users.models import MyUser
from products.models import category,Product
from rest_framework import serializers
from .models import Coupon,user_coupon,Product_offer
from rest_framework.authentication import authenticate
class MyAdminserializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'


class Mycategory (serializers.ModelSerializer):
    class Meta:
        model = category
        fields ='__all__'

class Myproduct(serializers.ModelSerializer):
   
    class Meta:
        model = Product
        fields='__all__' 

      
class MyCoupon(serializers.ModelSerializer):
    class Meta:
        model=Coupon
        fields='__all__'


class MYUSERcoupon(serializers.ModelSerializer):
    class Meta:
        model = user_coupon
        fields = '__all__'


class Myusercoupon(serializers.ModelSerializer):

    username = serializers.CharField(source='user_name.username')
    couponname = serializers.CharField(source='cpn_code.coupon_code')
    class Meta:
        model = user_coupon
        fields = ['couponname', 'status', 'username']
class Myproductoffer(serializers.ModelSerializer):
    class Meta:
        models=Product_offer
        fields='__all__'