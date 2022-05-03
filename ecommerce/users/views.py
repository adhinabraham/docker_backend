

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from .models import MyUser
from .serializer import MyMobileserializer, MyUserSerializer
from django.contrib.auth.hashers import make_password
from os import chmod
import os
from django.http import Http404
from django.contrib import messages
from twilio.rest import Client
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .private import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_SERVICE_SID









# Create your views here.
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # print("this istoken")
    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)

    #     # Add custom claims
    #     token['username'] = user.username
    #     token['message']="hello world"
    #     # ...

    #     return token

    def validate(self, attrs):
        data = super().validate(attrs)

        data['username']=self.user.username
        data['email']=self.user.email
        data['id']=self.user.id

        # refresh = self.get_token(self.user)

        # data["refresh"] = str(refresh)
        # data["access"] = str(refresh.access_token)

        # if api_settings.UPDATE_LAST_LOGIN:
        #     update_last_login(None, self.user)

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# <-------------------------usersiginup view-------------------------->
class Signup(APIView):
    
    def post(self,request):
        serializer = MyUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("saved ayyeee")
            return Response(serializer.data, status=status.HTTP_201_CREATED , )
         
        print("",serializer.errors)
        # response = JsonResponse(serializer.errors, status=500)
        return Response(serializer.errors,status=status.HTTP_502_BAD_GATEWAY)

   
class Otp(APIView):

    def get_mobile(self,num):
     try:
            return MyUser.objects.get(mobile_number=num)
     except MyUser.DoesNotExist:
            raise Http404 
   
    def post (self,request):
        print ("this is otp")
        mobile =request.data
        num=mobile['mobile_number']
        print(num)
        data=self.get_mobile(num)
   
        if data is not None:
           
            user_mobile='+91'+num
            print (user_mobile)
            account_sid = TWILIO_ACCOUNT_SID
            auth_token = TWILIO_AUTH_TOKEN
            Services=TWILIO_SERVICE_SID
            client = Client(account_sid, auth_token)
            verification = client.verify \
                .services(Services) \
                .verifications \
                .create(to=user_mobile, channel='sms')
            print(verification.status)
            messages.info(request,'Please enter the otp you have recieved on your mobile')
               
            return Response( status=status.HTTP_201_CREATED )
        
        return Response(status=status.HTTP_502_BAD_GATEWAY)


    #  number=mobile['mobile_number']
    #  print (mobile['mobile_number'])
    #  user_mobile='+91'+number
    #  print (user_mobile)
    #  account_sid = TWILIO_ACCOUNT_SID
    #  auth_token = TWILIO_AUTH_TOKEN
    #  Services=TWILIO_SERVICE_SID
    #  client = Client(account_sid, auth_token)
    #  verification = client.verify \
    #      .services(Services) \
    #      .verifications \
    #      .create(to=user_mobile, channel='sms')

    #  print(verification.status)
    #  messages.info(request,'Please enter the otp you have recieved on your mobile')
    #  return Response('double_varification.html')
     
class otpverification(APIView):
    # def get_mobile(self,num):
    #  try:
    #         return MyUser.objects.get(mobile_number=num)
    #  except MyUser.DoesNotExist:
    #         raise Http404 


    def post(self,request):
        otp=request.data
        print (otp,"this is otp and and here ...")
        otpcode =otp['otp']
        number=otp['mobile_number']
        
        
        usermobile="+91"+number
        print(otpcode)
        # account_sid = os.environ['TWILIO_ACCOUNT_SID']
        # auth_token = os.environ['TWILIO_AUTH_TOKEN']
        account_sid=TWILIO_ACCOUNT_SID
        auth_token=TWILIO_AUTH_TOKEN
        Services=TWILIO_SERVICE_SID
        client = Client(account_sid, auth_token)

        verification_check = client.verify \
                                .services(Services) \
                                .verification_checks \
                                .create(to=usermobile, code=otpcode)

        print(verification_check.status)

        if verification_check.status == 'approved':

          return Response(status=status.HTTP_202_ACCEPTED)
        else:
            print ("not a valid otp")
            return Response(status=status.HTTP_502_BAD_GATEWAY)


class Userprofile(APIView):
    def post (self,request):
        print ("user profile")
        userid=request.data["id"]
        user=MyUser.objects.get(id=userid)
        print (user)
        userserial=MyUserSerializer(user)
       
        return Response (userserial.data)
  
    
    # twilio code for otp generation


    def patch(self,request):
        print ("user edit profile ")
        userid=request.data["id"]
        print (userid)
        user = MyUser.objects.get(id=userid)
        user.username=request.data['username']
        user.email=request.data['email']
        user.mobile_number=request.data['phone']
        user.save ()
        print("data is saved ")
        
        return Response ("this is saved userdata")

 

   

     
class userdashbord(APIView):
    def get(self,request):
        users=MyUser.objects.count()
        print(users)
        return Response ({"user":users})

class Username(APIView):
    def post(self,request):
        user=request.data["id"]
        username=MyUser.objects.get(id=user)
        userserial=MyUserSerializer(username)
        return Response ({"data":userserial.data})


# {"username":"niyas",
# "password":"12345",
#  "mobile_number":"0000000000",
#  "email":"adhinabraham@gmail.com"}
# {"mobile_number":"7012682523"}
# {"otp":""}