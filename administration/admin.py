from django.contrib import admin
from .models import Brand, Categories, Color, Products, Size, Variants

# Register your models here.
class ProductsListAdmin(admin.ModelAdmin):
    list_display = ('id','prd_name','prd_image','prd_price')

admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(Size)
admin.site.register(Categories)
admin.site.register(Products,ProductsListAdmin)
admin.site.register(Variants)
