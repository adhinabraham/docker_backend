
from products.models import Product
from users.models import MyUser
from django.db import models


# Create your models here.
class Cart(models.Model):
    product_id = models.ForeignKey(Product, related_name='products',on_delete=models.CASCADE)
    username = models.ForeignKey(MyUser,on_delete=models.CASCADE,blank=True,null=True)
    product_stock = models.PositiveBigIntegerField(null=True, blank=True, default=0)
    sub_total = models.PositiveBigIntegerField(null=True, blank=True, default=0)
    guest_token = models.CharField(blank=True, null=True, max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    



   