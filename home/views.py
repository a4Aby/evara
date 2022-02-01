from itertools import product
import json
from multiprocessing.connection import Connection
from statistics import variance
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import render
from administration.models import Brand, Categories, Color, ProductImages, Products, Size, Variants
from administration.views import categories
from datetime import datetime,timedelta
from django.core import serializers
from django.http.response import JsonResponse

from store.models import Customer, Order, OrderItem, Wishlist
from store.utils import cartData

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
def chooseColor(request):
    choosedchildProduct = Products.objects.get(id = request.POST['childProduct'])
    childProduct = Products.objects.filter(proParent_id = choosedchildProduct.proParent_id)
    
    ChildVariant = Variants.objects.filter(product = choosedchildProduct.id)
    images = ProductImages.objects.filter(product = choosedchildProduct.id)
    lowestVariant = Variants.objects.raw('SELECT * FROM administration_variants WHERE product_id = %s ORDER BY price ASC LIMIT 1',(choosedchildProduct.id,))
    
    data = {
        'productDet' : choosedchildProduct,
        'childProduct' : childProduct,
        'lowestChildVariant' : ChildVariant,
        'images' : images,
        'imagesCount' : images.count(),
        'lowestVariant' : lowestVariant,
    }
    return render(request,'productDetialsModel.html',data)
def chooseVariant(request):
    variant = Variants.objects.filter(id = request.POST['variant_id'])
    for variantval in variant:
        # print(variantval.offerPercentage)
        jsonData = {
            'price' : variantval.price,
            'strike_price' : variantval.strike_price,
            'gst' : variantval.gst,
            'currency' : variantval.currency,
            'width' : variantval.width,
            'height' : variantval.height,
            'weight' : variantval.weight,
            'shipping_fee' : variantval.shipping_fee,
            'availabilityCount' : variantval.availabilityCount,
            # 'offerPercentage' : variantval.offerPercentage,
        }
    return JsonResponse(jsonData,safe=False)

def productDetials(request):
    childProduct = Products.objects.filter(proParent_id = request.POST['productId'])
    lowestChild = Products.objects.raw('select * from administration_products where prd_price > 0 and proParent_id = %s order by prd_price asc limit 1',[request.POST['productId']])
    for child in lowestChild:
        lowestChildVariant = Variants.objects.filter(product = child.id)
        product = Products.objects.get(id = child.id)
        images = ProductImages.objects.filter(product = child.id)
        lowestVariant = Variants.objects.raw('SELECT * FROM administration_variants WHERE product_id = %s ORDER BY price ASC LIMIT 1',(child.id,))
    
    
    data = {
        'productDet' : product,
        'childProduct' : childProduct,
        'lowestChildVariant' : lowestChildVariant,
        'images' : images,
        'imagesCount' : images.count(),
        'lowestVariant' : lowestVariant,
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
    cartTotal = 0

    data = cartData(request)
    cartTotal = data['cartItems']
    order = data['order']
    items = data['items']
    
    if request.user.is_authenticated :
        customer, created = Customer.objects.get_or_create(user=request.user,defaults={'name': request.user.username,'email':request.user.email})
        Wishlistcount = Wishlist.objects.filter(customer = customer).count()
        order = Order.objects.filter(customer=customer,complete = 0)
        # cartTotal = OrderItem.objects.filter(order=order).count()
    
    categories = Categories.objects.all()
    brand = Brand.objects.all()
    content = {
        'parent_category':all_categories,
        'categories':categories,
        'all_products' : all_products,
        'new_arrivals' : new_arrivals,
        'Wishlistcount' : Wishlistcount,
        'cartTotal' : cartTotal,
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
    