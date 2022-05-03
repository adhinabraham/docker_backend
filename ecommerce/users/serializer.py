from wsgiref.validate import validator
from  .models import MyUser
from rest_framework import serializers



class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = "__all__"
        
    
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class MyMobileserializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ["mobile_number"]
        



