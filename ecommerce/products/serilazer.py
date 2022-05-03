from rest_framework import serializers
from .models import Product,category



class MyproductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields='__all__' 


class MyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = '__all__'
