from django.contrib import admin
from .models import Product,category,subcategory

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display        = ('category_name','slug',)


# Register your models here.
admin.site.register(Product)
admin.site.register(category,CategoryAdmin)
admin.site.register(subcategory)
