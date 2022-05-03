from cgitb import reset, text
from fileinput import filename
from itertools import count, product
from mmap import PAGESIZE
from sys import flags
from unittest import result
from urllib.parse import uses_relative
from wsgiref.util import request_uri
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from .serializer import OrderAddressSerializer, OrderSerializer, OrderAdminserializer, OrdernumberSerializer
from .models import Address, Order, Ordernumber
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse
from cart.models import Cart
from datetime import date
import random
import string
import datetime
import itertools
import razorpay
import json
import xlwt
from django.http import HttpResponse
from django.utils.timezone import utc
from django .http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from io import BytesIO
from xhtml2pdf import pisa
import os



# Create your views here.


class OrderAddress(APIView):

    def get(self, request):
        print("this is get")
        data = Address.objects.all()
        print("pro")
        seriail = OrderAddressSerializer(data, many=True)
        return Response(seriail.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrderAddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("saved ayyeee")
            return Response(serializer.data, status=status.HTTP_201_CREATED, )

        print("", serializer.errors)

        return Response(serializer.errors, status=status.HTTP_502_BAD_GATEWAY)


class ordernumber_generation(APIView):
    def get(self, request):
        print("this is otp")
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")
        orderno = Ordernumber()

        orderno.save()
        orderno.order_no = current_date + str(orderno.id)
        orderno.save()
        print(orderno)

        return Response({"num": orderno.order_no})


class Orderplaced(APIView):
    def post(self, request):
        print("order palced ")

        userid = request.data["username"]
        ordernum = request.data["order_number"]
        orderid = Ordernumber.objects.get(order_no=ordernum)
        Idorder = orderid.id

        request.data['order_number'] = Idorder

        items = Cart.objects.filter(username=userid)
        order = Order()

        for i in items:
            print(i.product_id_id)
            request.data["product"] = i.product_id_id
            request.data["product_stock"] = i.product_stock
            print("this is product assigned")
            print(request.data, "this is request.data")
            seril = OrderSerializer(data=request.data)
            if seril.is_valid(raise_exception=True):
                seril.save()
                print("this is porduct")
            else:
                return Response("this is not a valid data")

        print("for loop is completed")
        return Response({"status": "true"})

    def get(self, request):
        print("this is get")
        data = Order.objects.all()
        print("pro")
        seriail = OrderAdminserializer(
            data, many=True, context={'request': request})
        return Response(seriail.data, status=status.HTTP_200_OK)

    def patch(self, request):
        print("this is patch ")
        orderid = request.data["orderid"]
        productid = request.data["productid"]
        orderstatus = request.data["status"]
        item = Order.objects.get(order_number=orderid, product=productid)

        item.status = orderstatus
        item.save()
        serial = OrderSerializer(data=item)
        print(serial)
        return Response(" saved ")


class Userorder(APIView):

    def post(self, request):
        print('this is fucking ')
        username = request.data["username"]
        print(username)
        data = Order.objects.filter(username=username)
        useritems = OrderAdminserializer(
            data, many=True, context={'request': request})
        return Response(useritems.data)

    def patch(self, request):
        username = request.data['id']
        fronendstatus=request.data['status']
        if fronendstatus == "cancel":
            print(id)
            data = Order.objects.get(id=username)
            print(data)
            data.status = "cancel"
            print(data.status)
            data.save()
            return Response("changed")
        if fronendstatus == 'return':
            print(id)
            data = Order.objects.get(id=username)
            print(data)
            data.status = "return"
            print(data.status)
            data.save()
            return Response("changed")


class ordernumberlist(APIView):

    def post(self, request):
        print("ordre number function")

        username = request.data["username"]
        data = Order.objects.filter(username=username)
        print(type(data))
        print(data)
        useritems = OrdernumberSerializer(
            data, many=True,)

        return Response(useritems.data)


# <........................razorpayintegration.....................>
class razorpayintegration(APIView):
    def post(self, request):
        amount = request.data['total']
        print(amount)
        amounttotal=int(amount)
        print(amounttotal)
        # name=request.data['username']

        client = razorpay.Client(
            auth=('rzp_test_G8TzKLyrRHqa66', 'VOznj2MYGgNgZwq5FyGdfH5t'))

        payment = client.order.create({"amount": amount * 100,
                                       "currency": "INR",
                                       "payment_capture": "1"})
        print(payment)
        print("this is  razarpay")

        return Response({'payment': payment})


@api_view(['POST'])
def handle_payment_success(request):
    print("this iis razorpay order is palced in database ")
    # request.data is coming from frontend
    res = json.loads(request.data["response"])

    """res will be:
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    this will come from frontend which we will use to validate and confirm the payment
    """

    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]

    # get order by payment_id which we've created earlier with isPaid=False
    order = Order()

    # we will pass this whole data in razorpay client to verify the payment
    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }

    client = razorpay.Client(
        auth=(('rzp_test_G8TzKLyrRHqa66'), ('VOznj2MYGgNgZwq5FyGdfH5t')))

    # checking if the transaction is valid or not by passing above data dictionary in
    # razorpay client if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)

    if check is not None:
        print("Redirect to error url or error page")
        return Response({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    # order.isPaid = True

    order.save()
    print("ordersaved")

    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data)


class ordersum(APIView):
    def get(self, request):
        price = 0
        all = Order.objects.filter(status="Develiverd")
        for i in all:
            print(i.product.price)
            price = price+i.product.price
        print(price)
        return Response({"price": price})


class Nooforder(APIView):
    def get(self, request):

        all = Order.objects.all().count()

        return Response({"count": all})


class lastfiveorder(APIView):
    def get(self, request):
        print("last order ")
        last_ten = Order.objects.order_by('-id')[:5]
        print(last_ten,
              "this is last oder in order")
        seriallast_ten = OrderAdminserializer(last_ten, many=True)

        return Response(seriallast_ten.data)


@api_view(['GET'])
def export_users_xls(request):
    print("this is xls page ")
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Username',  'product', 'total']

    for col_num in range(len(columns)):
        # at 0 row 0 column
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Order.objects.all().values_list(
        'username', 'product', 'total')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    print(wb)

    return Response("response")


class Salesreport(APIView):
    def post(self, request):

        data = request.data["sales"]
        today = datetime.date.today()
        month = datetime.date.today()-datetime.timedelta(days=30)
        week = datetime.date.today()-datetime.timedelta(days=5)

        if data == "month":

            orders = Order.objects.filter(date__range=(month, today))

            print(orders)
            serialmonth = OrderAdminserializer(orders, many=True)
            print(serialmonth)
            print("this is month ")

            return Response(serialmonth.data)

        if data == "week":
            print("this is week")

            orderweek = Order.objects.filter(date__range=(week, today))

            serialweek = OrderAdminserializer(orderweek, many=True)
            print(serialweek)
            print("this is week")
            return Response(serialweek.data)


# class pdfexport (APIView):
#     def get(self, request):
#         print("this is pdf ")
#         buf = io.BytesIO()
#         c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
#         textob = c.beginText()
#         textob.setTextOrigin(inch, inch)
#         textob.setFont("Helvetica", 12)
#         lines=Order.objects.all()
#         # data = {
#         #                 "orderid":lines.id,
#         #                 "username":lines.username,
#         #                 "products":lines.products,
#         #                 "price":lines.price,
#         #                 "data":lines.date,
#         #                 "status":lines.status
#         #             }
#         # pdfdata=data
#         for i in lines:
#             textob.textLine(i)
#         c.drawText(textob)
#         c.showPage()
#         c.save()
#         buf.seek(0)
#         return FileResponse(buf,as_attachment=True,filename='venue.pdf')



        

# class execl(APIView):
#     def get(self,request):
#         order_data = Order.objects.all()
#         response = HttpResponse(content_type='application/ms-excel')
#         response['Content-Disposition'] = 'attachment; filename=ShopifyOrder'+'.xls'
#         wb = xlwt.Workbook(encoding='utf-8')
#         ws = wb.add_sheet('Sales Report')
#         row_num = 0
#         font_style = xlwt.XFStyle()
#         font_style.font.bold = True
#         columns = ['Order No', 'Name', 'Number Of Products',
#                 'Order Date', 'Amount', 'Payment Type']

#         for col_num in range(len(columns)):
#             ws.write(row_num, col_num, columns[col_num], font_style)

#         font_style = xlwt.XFStyle()

#         rows = order_data.values_list(
#             'order_order_number', 'userusername', 'quantity', 'created_at', 'paymentamount_paid', 'payment_payment_method'
#         )

#         for row in rows:
#             row_num = row_num + 1

#             for col_num in range(len(columns)):
#                 ws.write(row_num, col_num, str(row[col_num]), font_style)
#         wb.save(response)

#         return response
        
#     def render_to_pdf(context_dict={}):
#         reust=BytesIO()
#         pdf=pisa.pisaDocument(BytesIO(result))
#         return None

        # return Response ({"data":"saved"})

#  {"status":"item_shipped","orderid":"2022032169","productid":"29"}
#instance.email = validated_data.get('email', instance.email)


# # {"userid":"31","address":3,"payment_method":"COD","order_number":2022201}

        # return Response ({"data":"notsaved"})


# class Ordermanage(APIView):
# {"userid":31}


#  {"full_name":"zayan malik","mobile":"7012682523","state":"kerala","city":"kalladikode","district":"palakkad","address_line1":"puthenparambil"}
