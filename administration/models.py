from django.db import models
from django.db.models.fields import NullBooleanField

# Create your models here.
class Categories(models.Model):
    cat_name = models.CharField(max_length=255)
    cat_slug = models.CharField(max_length=255)
    parent_category = models.ForeignKey('self',related_name='children',on_delete=models.CASCADE,blank=True,null=True)
    cat_description = models.TextField()
    cat_status = models.CharField(max_length=10,default='1')
    cat_order = models.CharField(max_length=10,default='1')

    def __str__(self):
        return self.cat_name


class Products(models.Model):
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
    prd_sub_category = models.CharField(max_length=100,default='')
    prd_tags = models.CharField(max_length=100,default='')
    prd_status = models.CharField(max_length=10,default='1')
    prd_order = models.CharField(max_length=10,default='1')
    prd_image = models.ImageField(null=True,blank=True, upload_to='uploads/')
    prd_created_on = models.DateField(auto_now_add=True)