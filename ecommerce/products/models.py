from django.db import models

# Create your models here.
class category(models.Model):
    category_name = models.CharField(max_length=100,unique=True)
    slug = models.CharField(max_length=100,unique=True)
    description = models.TextField(max_length=250)
    offerstatus = models.BooleanField(null=True, blank=True,default=False)

    def __str__(self):
        return self.category_name

class subcategory(models.Model):
    sub_category_name = models.CharField(max_length=100)
    category_name = models.ForeignKey(category,on_delete=models.CASCADE)
    description = models.TextField(max_length=250)
    slug = models.CharField(max_length=100,unique=True)
    

    def __str__(self):
        return self.sub_category_name

class Product(models.Model):
   
    productname = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='pics',blank = True,null =True)
    image1 = models.ImageField(upload_to='pics',blank = True,null =True)
    image2 = models.ImageField(upload_to='pics',blank = True,null =True)
    image3 = models.ImageField(upload_to='pics',blank = True,null =True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # brand_name = models.ForeignKey(brand,on_delete=models.CASCADE)
    category_name = models.ForeignKey(category,on_delete=models.CASCADE,blank=True,null=True)
    price2 = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    sub_catagory_name = models.ForeignKey(subcategory,on_delete=models.CASCADE,blank=True,null=True)
    amount_in_stock = models.IntegerField(blank=True,default=0,help_text=("Amount in stock"))
    offer_name = models.CharField(max_length=50,blank=True,null=True)
    offerstatus = models.BooleanField(null=True,blank=True)
    offerpercentage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.productname
        
