from django.contrib import admin
from .models import Categories, Products

# Register your models here.
class ProductsListAdmin(admin.ModelAdmin):
    list_display = ('id','prd_name','prd_image','prd_price')

admin.site.register(Categories)
admin.site.register(Products,ProductsListAdmin)
