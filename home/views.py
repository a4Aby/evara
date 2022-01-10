from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import render
from administration.models import Categories, Products
from administration.views import categories
from datetime import datetime,timedelta

# Create your views here.
def index(request):
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
    # return HttpResponse(all_products)
    # print(all_products)
    return render(request,'index.html',content)

def items(request):
    return render(request,'items.html')

def checkout(request):
    return render(request,'checkout.html')

def about(request):
    return render(request,'about.html')
    