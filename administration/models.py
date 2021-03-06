from email.mime import image
from itertools import product
from re import T
from unicodedata import name
from django.db import models
from django.db.models.fields import NullBooleanField
from django.utils.safestring import mark_safe

# Create your models here.
class Categories(models.Model):
    cat_name = models.CharField(max_length=255)
    cat_slug = models.CharField(max_length=255)
    parent_category = models.ForeignKey('self',related_name='children',on_delete=models.CASCADE,blank=True,null=True)
    cat_description = models.TextField()
    cat_status = models.CharField(max_length=10,default='1')
    cat_order = models.CharField(max_length=10,default='1')
    cat_image = models.CharField(max_length=100,default='')
    cat_image = models.ImageField(null=True,blank=True, upload_to='uploads/')


    def __str__(self):
        return self.cat_name
class Brand(models.Model):
    brandName = models.CharField(max_length=100,default='')
    brandLogo = models.ImageField(null=True,blank=True, upload_to='uploads/')
    status = models.IntegerField(default=1)
    def __str__(self):
        return self.brandName
class Color(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100,blank=True,null=True)
    def __str__(self):
        return self.name
    def color_tag(self):
        if self.code is not None:
            return mark_safe('<input type="color" disabled value="{}" ></input>'.format(self.code))

class Size(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
class Products(models.Model):
    proParent = models.ForeignKey('self',related_name='children',on_delete=models.CASCADE,blank=True,null=True)
    prd_name = models.CharField(max_length=255,default='')
    prd_description = models.TextField(default='')
    prd_price = models.FloatField(default=0)
    prd_strike_price = models.FloatField(default=0)
    prd_currency = models.CharField(max_length=100,default='')
    prd_gst = models.CharField(max_length=100,default='')
    prd_cod_available = models.CharField(max_length=100,default='0')
    prd_width = models.CharField(max_length=100,default='')
    prd_height = models.CharField(max_length=100,default='')
    prd_weight = models.CharField(max_length=100,default='')
    prd_shipping_fee = models.CharField(max_length=100,default='')
    prd_image = models.CharField(max_length=100,default='')
    prd_parent_category = models.CharField(max_length=100,default='')
    prd_sub_category = models.ForeignKey(Categories,on_delete=models.CASCADE,blank=True,null=True)
    prd_tags = models.CharField(max_length=100,default='')
    prd_status = models.CharField(max_length=10,default='1')
    prd_order = models.CharField(max_length=10,default='1')
    prd_image = models.ImageField(null=True,blank=True, upload_to='uploads/')
    prd_created_on = models.DateField(auto_now_add=True)
    prd_is_featured = models.CharField(max_length=10,default='0')
    prd_is_popular = models.CharField(max_length=10,default='0')
    prd_brand = models.CharField(max_length=100,default='')
    prd_reviewsCount = models.IntegerField(default=0)
    prd_oferPercentage = models.FloatField(max_length=10,default=0)
    prd_color = models.CharField(max_length=100,default='', null=True)
    prd_size = models.CharField(max_length=100,default='', null=True)
    prd_availabilityCount = models.IntegerField(default=1, null=True)
    prd_BrandTable = models.ForeignKey(Brand,on_delete=models.CASCADE,blank=True,null=True)
    prd_sizeTable = models.ForeignKey(Size,on_delete=models.SET_NULL, null=True)
    prd_colorTable = models.ForeignKey(Color,on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.prd_name
    def offerPercentage(self):
        return (self.prd_price/self.prd_strike_price)*100

class ProductImages(models.Model):
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True,blank=True, upload_to='uploads/')

class Variants(models.Model):
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField(default=0)
    strike_price = models.IntegerField(default=0)
    gst = models.CharField(max_length=100,default='')
    currency = models.CharField(max_length=100,default='')
    width = models.CharField(max_length=100,default='')
    height = models.CharField(max_length=100,default='')
    weight = models.CharField(max_length=100,default='')
    shipping_fee = models.CharField(max_length=100,default='')
    sizeTable = models.ForeignKey(Size,on_delete=models.SET_NULL, null=True)
    availabilityCount = models.CharField(max_length=100,default='')

    def offerPercentage(self):
        return (self.price/self.strike_price)*100