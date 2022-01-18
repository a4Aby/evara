from django.http.response import HttpResponse
from django.shortcuts import render
from administration.models import Categories
from administration.models import Products
# from store.models import Wishist
from django.http import JsonResponse
import json
from .utils import *

# Create your views here.

def items(request,cat_id):
    product_list = Products.objects.filter(prd_sub_category = cat_id)
    #customer = request.user.customer
    data = cartData(request)
    cartTotal = data['cartItems']
    order = data['order']
    
    all_categories = Categories.objects.filter(parent_category=None)
    all_products = Products.objects.filter()
    categories = Categories.objects.all()

    context = {
        'parent_category':all_categories,
        'categories':categories,
        'all_products' : all_products,
        'items' : product_list,
        'cartTotal' : cartTotal,
        'items_count' : product_list.count()
    }
    return render(request,'store.html',context)

def cart(request):
    data = cartData(request)
    cartTotal = data['cartItems']
    order = data['order']
    items = data['items']
    
    all_categories = Categories.objects.filter(parent_category=None)
    all_products = Products.objects.filter()
    categories = Categories.objects.all()

    context = {
        'parent_category':all_categories,
        'categories':categories,
        'all_products' : all_products,
        'items' : items,
        'cartTotal' : cartTotal
    }
    return render(request,'cart.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)
    print(request.user)
    #return HttpResponse(request)
    #if request.user.is_authenticated:
    customer = request.user.customer
    #customer, created = Customer.objects.get_or_create(user=request.user)

    #print(customer)
    product = Products.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def addWishList(request):
    data = {}
    product = Products.objects.get(id=request.POST['productId'])
    customer, created = Customer.objects.get_or_create(user=request.user,defaults={'name': request.user.username,'email':request.user.email})
    # WishlistItems, created = Wishlist.objects.get_or_create(order=order, product=product)

    checkW = Wishlist.objects.filter(customer = customer, product= product).count()
    Wishlistcount = Wishlist.objects.filter(customer = customer).count()
    # checkW = 1
    if checkW > 0:
        data={
            'staus' : True,
            'message': 'Already Added',
            'Wishlistcount' : Wishlistcount,
        }
    else:
        WishlistItems, created = Wishlist.objects.get_or_create(customer=customer, product=product)

        # Wishlist = Wishlist.objects.create(
        #     customer=customer,
        #     product=product
        #     )
        data={
            'staus' : True,
            'message': 'Added To Wish List',
            'Wishlistcount' : Wishlistcount,
        }

    return JsonResponse(data)
