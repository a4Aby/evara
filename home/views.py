from itertools import product
import json
from multiprocessing.connection import Connection
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import render
from administration.models import Brand, Categories, Color, Products, Size
from administration.views import categories
from datetime import datetime,timedelta
from django.core import serializers
from django.http.response import JsonResponse

from store.models import Customer, Wishlist

# Create your views here.
def itemList(request):
    list = []

    if 'q' in request.GET:
        products = Products.objects.filter(prd_name__startswith=request.GET.get('q'))
        if products is not None:
            for product in products:
                list.append(product.prd_name)
        else:
            list.append('No Data Found')
    else:
        list.append('No Data Found')
    
    return JsonResponse(list,safe=False)
def productVariants(request):
    product = Products.objects.filter(id = request.POST['productId'])
    childProduct = Products.objects.filter(proParent_id = request.POST['parent'],prd_sizeTable_id =request.POST['size'],prd_colorTable_id =request.POST['color'] )
    
    availableColorids = childProduct.values_list('prd_colorTable_id', flat=True).distinct()
    availableColor = Color.objects.filter(id__in=availableColorids)

    availableSizeids = childProduct.values_list('prd_sizeTable_id', flat=True).distinct()
    availableSize = Size.objects.filter(id__in=availableSizeids)
    
    data = {
        'productDet' : product,
        'childProduct' : childProduct,
        'size' : availableSize,
        'color' : availableColor,
    }
    return render(request,'productDetialsModel.html',data)
    return JsonResponse(data,safe=False)   
def productDetials(request):

    product = Products.objects.filter(id = request.POST['productId'])
    # childProduct = Products.objects.filter(proParent_id = request.POST['productId']) | Products.objects.filter(id = request.POST['productId'])
    childProduct = Products.objects.filter(proParent_id = request.POST['productId'])
    availableSizeids = childProduct.values_list('prd_sizeTable_id', flat=True).distinct()
    availableSize = Size.objects.filter(id__in=availableSizeids)
    availableColorids = childProduct.values_list('prd_colorTable_id', flat=True).distinct()
    availableColor = Color.objects.filter(id__in=availableColorids)

    data = {
        'productDet' : product,
        'childProduct' : childProduct,
        'size' : availableSize,
        'color' : availableColor,
    }
    return render(request,'productDetialsModel.html',data)

def childproductDetials(request):
    product = Products.objects.filter(id = request.POST['productId'])
    currentProduct = Products.objects.get(id = request.POST['productId'])

    if currentProduct.proParent_id is None:
        childProduct = Products.objects.filter(proParent_id = request.POST['productId']) | Products.objects.filter(id = request.POST['productId'])
    else:
        childProduct = Products.objects.filter(proParent_id = currentProduct.proParent_id) | Products.objects.filter(id = currentProduct.proParent_id)
    
    availableSize = childProduct.values_list('prd_size', flat=True).distinct()
    print(currentProduct.id)
    data = {
        'productDet' : product,
        'childProduct' : childProduct,
        'size' : {"S","M","L","XL","XXL"},
        'availableSize' :availableSize,
    }
    return render(request,'productDetialsModel.html',data)


def index(request):
    all_categories = Categories.objects.filter(parent_category=None)
    all_products = Products.objects.filter(proParent_id=None)
    new_arrivals = Products.objects.filter(proParent_id=None,prd_created_on__gte=datetime.now()-timedelta(days=7) )
    Wishlistcount = 0
    if request.user.is_authenticated :
        customer, created = Customer.objects.get_or_create(user=request.user,defaults={'name': request.user.username,'email':request.user.email})
        Wishlistcount = Wishlist.objects.filter(customer = customer).count()
    
    categories = Categories.objects.all()
    brand = Brand.objects.all()
    content = {
        'parent_category':all_categories,
        'categories':categories,
        'all_products' : all_products,
        'new_arrivals' : new_arrivals,
        'Wishlistcount' : Wishlistcount,
        'brands':brand,
    }
    # return HttpResponse(all_products)
    # print(all_products)
    return render(request,'index.html',content)

def items(request):
    return render(request,'items.html')

def checkout(request):
    return render(request,'checkout.html')

def about(request):
    all_categories = Categories.objects.filter(parent_category=None)
    all_products = Products.objects.filter()
    new_arrivals = Products.objects.filter(prd_created_on__gte=datetime.now()-timedelta(days=7) )

    categories = Categories.objects.all()

    content = {
        'parent_category':all_categories,
        'categories':categories,
        'all_products' : all_products,
        'new_arrivals' : new_arrivals,
    }
    return render(request,'about.html',content)
    