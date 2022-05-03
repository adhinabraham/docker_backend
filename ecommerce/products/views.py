from dataclasses import dataclass
from re import S

from urllib import request
from django.shortcuts import render
from django.urls import is_valid_path

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404, JsonResponse
from .models import Product,category
from .serilazer import MyproductSerializer,MyCategorySerializer
from rest_framework import status


class productlist(APIView):
    def get(self, request):
        print("product list")
        product = Product.objects.all()
        Serializer = MyproductSerializer(
            product, many=True, context={'request': request})
        print(Serializer.data)

        return Response(Serializer.data)


class showproduct(APIView):
    serializer_class = MyproductSerializer
    def get(self,request,pk):
        data=Product.objects.get(pk=pk)
        seril = self.serializer_class(data, context={'request': request})
        serialized_data = seril.data
        print(serialized_data)
        return Response(serialized_data)
        # return Response({'msg':'request received herer'})




class productoffer(APIView):
    def patch(self,request):
        productname=request.data["productname"]
        discountpert = request.data["discountpercentage"]
        offername = request.data["offername"]
       
        discountper=int(discountpert)
        print(type(discountper))
        if discountper>90:
            return Response ("not valid offer",status=status.HTTP_400_BAD_REQUEST)



        productid=Product.objects.get(productname=productname)
        if productid.offerstatus==True:
            return Response ("product offer already applied  ")
        print(productid,"productid ")
        discountpercentage=int(discountper)
        actualprice=productid.price
        price2=productid.price2
        price2=actualprice
        print(price2)
        discountprice=actualprice*discountpercentage/100
        print(discountprice)
        actualprice=price2-discountprice

        print(actualprice)
        productid.price=actualprice
        productid.price2=price2
        productid.offerstatus=True
        productid.offer_name=offername
        productid.offerpercentage = discountpercentage
        
        print(productid.price, productid.price2,
              productid.offerstatus, productid.offer_name)
        productid.save()
        
        return Response("offer applied to product")
    def get(self,request):
      
        product = Product.objects.filter(offerstatus=True)
        Serializer = MyproductSerializer(
            product, many=True, context={'request': request})
        print(Serializer.data)

        return Response(Serializer.data)

    def post(self,request):
        pk=request.data["id"]
        product=Product.objects.get(id=pk)
        print(product)
        productprice2= product.price2
        print(productprice2)
        productprice=product.price
        print(productprice)
        product.price = productprice2

        product.offerstatus=False
        product.save()
        return Response("offer cancled")
        
class Categoryoffer(APIView):
   def post(self,request):
       categoryid = request.data["categoryname"]
       discountpert = request.data["discountpercentage"]
       offername = request.data["offername"]
       discountper=int(discountpert)
       print(type(discountper))
       if discountper>90:
           print("not valid ")
           return Response("not valid ",status=status.HTTP_400_BAD_REQUEST)
       

       item = category.objects.get(id=categoryid)
       if item.offerstatus == True:
           return Response ("already applied")
       item.offerstatus=True
      
       
       products = Product.objects.filter(category_name=categoryid)
       for i in products:
           print(i)
           if i.offerstatus==False:
                price1=i.price
                price2=i.price2
                price2=price1
                discountpercentage = int(discountper)
                discountprice = price1*discountpercentage/100
                price1 = price2-discountprice
                i.price=price1
                i.price2=price2
                i.offer_name = offername
                i.offerpercentage = discountpercentage
                i.offerstatus=True
                i.save()
                print("item saved")

       item.save()      
       print(products)
       return Response ("true")
   def patch(self,request):
       categoryid = request.data["id"]
       item = category.objects.get(id=categoryid)
       item.offerstatus = False
       products = Product.objects.filter(category_name=categoryid)
       for i in products:
            productprice2= i.price2
            print(productprice2)
            productprice=i.price
            print(productprice)
            i.price = productprice2

            i.offerstatus=False
            i.save()



       item.save()
       return Response("category items changed")
   def get(self,request):
       items=category.objects.filter(offerstatus=True)
       serialitems=MyCategorySerializer(items,many=True)
       return Response (serialitems.data)
    
class categoryitem(APIView):
    def get (self,request):
         items = category.objects.get(offerstatus=True)
       
         print(items.category_name)
         item = items.category_name
         return Response ({"item":item})

           




    




#    {"productname":"addidas","discountpercentage":"10","offername":"onamoffer"}