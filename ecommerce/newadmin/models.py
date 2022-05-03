from django.db import models
from users.models import MyUser
from products.models import Product


# Create your models here.


class Coupon(models.Model):
    min_rate = models.IntegerField()
    coupon_code = models.CharField(max_length=50, unique=True)
    percentage = models.PositiveIntegerField()
    expiry_date = models.DateField()
    description = models.CharField(max_length=50, blank=True)


class user_coupon(models.Model):
    user_name = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    cpn_code = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
   

class Product_offer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    offer_name = models.CharField(max_length=50)
    discount_value = models.PositiveIntegerField()
    expiry_date = models.DateField()



{"min_rate":500,"coupon_code":"12345","percentage":10,"expiry_date":"28-04-2022","description":"adipowlicoupon"}