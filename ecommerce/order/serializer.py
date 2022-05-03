from  .models import Address,Order,Ordernumber
from rest_framework import serializers
from users.models import MyUser


class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

class OrdernumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ordernumber
        fields = "__all__"


        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields="__all__"

 
class OrderAdminserializer(serializers.ModelSerializer):
    username =serializers.CharField(source='username.email')
    products = serializers.CharField(source='product.productname')  
    image_url = serializers.ImageField(source='product.image')
    price=serializers.CharField(source='product.price')
    # order_number=serializers.CharField
   
    # photo_url = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)


    class Meta:
        model = Order
        fields = ['id','username', 'products', 'price', 'image_url',
                  'order_number', 'date', 'status', 'product', 'product_stock']




class OrdernumberSerializer(serializers.ModelSerializer):
    ordernumber = serializers.CharField(source='order_number.order_no')
  
  
    class Meta:
        model = Order
        fields = ['ordernumber']


