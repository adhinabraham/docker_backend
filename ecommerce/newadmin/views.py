from ast import Delete, Not
from operator import is_not
from urllib import request
from xml.dom.minidom import TypeInfo
from django.shortcuts import render
from django.urls import is_valid_path
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from django.http import Http404
from users.models import MyUser
from .serilazer import MyAdminserializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework import generics
from products.models import category
from products.models import Product as ecomproduct
from .serilazer import Mycategory,Myproduct
from .models import Coupon
from .serilazer import MyCoupon,Myproductoffer
from rest_framework.parsers import MultiPartParser,FormParser








# Create your views here.
class Login (APIView):


    def get(self, request, format=None):
        print("this is admin ")
        user = MyUser.objects.all()
        
        serializer= MyAdminserializer(user ,many = True)
       
        return Response(serializer.data)
        return Response (status=status.HTTP_204_NO_CONTENT)



class Useredit(APIView):
    def get_object(self, pk):
        try:
            return MyUser.objects.get(id=pk)
        except MyUser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        print("user : ",user)
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return Response({"active_status":user.is_active})


class Category(APIView):
    def post(self,request,):
        
        print(request.data,"this is the data")
        item=Mycategory(data=request.data)
        print("hai")
        print(item)
        if item .is_valid(raise_exception=True):
            item.save()
            print('save ayee')
            return Response(item.data,status=status.HTTP_201_CREATED)
        else:
            return Response({"status":"false"})
         
    def get(self,request):
        print("this is category item")
        allitem=category.objects.all()
        serializeritem=Mycategory(allitem,many=True)
        return Response(serializeritem.data)




# <......................product add ...................>
class Product(APIView):
  
    def post(self,request):
        print("this is product")
        print(request.data)
       
        prodcutitem=Myproduct(data=request.data)
        i = request.data['category_name']
        categoryid=int(i)
        print(categoryid)

        print(type(categoryid))
        request.data['category_name'] = categoryid
       
   

       
        if prodcutitem.is_valid(raise_exception=True):
            prodcutitem.save()
            print("saved ")
            return Response({"status":"true"})
        else:
            print("thhis is not saved ")
            return Response({'status':'false'})

    def get(self,request):
        print("this is post")
        pro=ecomproduct.objects.all()
        print("pro")
        seriail=Myproduct(pro,many=True)
        return Response(seriail.data,status=status.HTTP_200_OK)


# <......................product delete ...................>       
class productdelete(APIView):
    def delete(self,request,pk):
        print("this is delete")

        data = ecomproduct.objects.get(id=pk)
        print(id)
        if data is not None:
           print("user endee")
           data.delete()
           pro=ecomproduct.objects.all()
           print("pro")
           seriail=Myproduct(pro,many=True)
           message=("data deleted")
           return Response(seriail.data)
        else:
            return Response("Product is  not found")
        
class coupongenerate(APIView):

    def post (self,request):
        print("coupon generation code ")
        coupon=request.data
        data=MyCoupon(data=coupon)
        print (data)
        if data.is_valid(raise_exception=True):
            data.save()
            return Response ("data is saved ")
        return Response ("not a valid coupon")



class Coupondelete(APIView):
    def post(self,request):
        id=request.data["id"]
        coupon=Coupon.objects.get(id=id)
        coupon.delete()
        return Response("deleted")




class Createdcoupon(APIView):
    def get(self,request):
        all=Coupon.objects.all()
        serilaall=MyCoupon(all,many=True)
        return Response(serilaall.data)

class productoffer(APIView):
    def post (self,request):
        productoffer=request.data
        productserial=Myproductoffer(data=productoffer,many=True)
        if productserial.is_valid(raise_exception=True):
            productserial.save()
            return Response ("productoffer applied ")






    # def delete(self,request):
