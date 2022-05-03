from django.urls import path
from . import views




urlpatterns = [
   
    path('orderaddress/',views.OrderAddress.as_view()),
    path('ordernumber/',views.ordernumber_generation.as_view()),
    path('orderplaced/',views.Orderplaced.as_view()),
    path('userorder/', views.Userorder.as_view()),
    path('orderid/', views.ordernumberlist.as_view()),
    path('ordersum/', views.ordersum.as_view()),
    path('nooforder/', views.Nooforder.as_view()),
    path('lastorder/', views.lastfiveorder.as_view()),
    path('salesreport/', views.Salesreport.as_view()),
    path('razorpay/', views.razorpayintegration.as_view()),
 
  
    path('razorpay/payment/success/',views.export_users_xls, name="payment_success")

    # path('showproduct/<int:pk>',views.showproduct.as_view()),
]