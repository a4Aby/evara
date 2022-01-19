import json
from multiprocessing.connection import Connection
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import render
from administration.models import Brand, Categories, Products
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
    
def productDetials(request):
    data = {}
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
    