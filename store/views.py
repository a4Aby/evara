from asyncio.windows_events import NULL
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from administration.models import Categories
from administration.models import Products
# from store.models import Wishist
from django.http import JsonResponse
import json
from .utils import *

# Create your views here.
def addCart(request):
    productId = request.POST['productId']
    action = request.POST.get('action','add')
    variant_id = request.POST.get('variant')
    quantity = int(request.POST.get('quantity',1))

    customer = request.user.customer

    product = Products.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    if variant_id:
        variant = Variants.objects.get(id = variant_id)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product,variant=variant)
    else:
        childProducts = Products.objects.raw('SELECT * FROM administration_products WHERE proParent_id = %s ORDER BY prd_price ASC LIMIT 1',(productId,))
        for childProduct in childProducts:
            variants = Variants.objects.raw('SELECT * FROM administration_variants WHERE product_id = %s ORDER BY price ASC LIMIT 1',(childProduct.id,))
            for variant in variants:
                orderItem, created = OrderItem.objects.get_or_create(order=order, product=childProduct,variant=variant)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + quantity)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - quantity)

    orderItem.save()


    if orderItem.quantity <= 0:
        orderItem.delete()
    data = {
        'message' : 'Cart Added',
        'count' : OrderItem.objects.filter(order=order).count()
    }

    return JsonResponse(data)
def productSearch(request,product):
    product_list = Products.objects.filter(prd_name = product)
    data = cartData(request)
    cartTotal = data['cartItems']
    order = data['order']
    
    all_categories = Categories.objects.filter(parent_category=None)
    all_products = Products.objects.filter()
    categories = Categories.objects.all()
    customer, created = Customer.objects.get_or_create(user=request.user,defaults={'name': request.user.username,'email':request.user.email})
    Wishlistcount = Wishlist.objects.filter(customer=customer).count()

    context = {
        'parent_category':all_categories,
        'categories':categories,
        'all_products' : all_products,
        'items' : product_list,
        'cartTotal' : cartTotal,
        'Wishlistcount' : Wishlistcount,
        'items_count' : product_list.count(),
    }
    return render(request,'store.html',context)

def items(request,cat_id):
    product_list = Products.objects.filter(prd_sub_category = cat_id, proParent_id=None)
    #customer = request.user.customer
    data = cartData(request)
    cartTotal = data['cartItems']
    order = data['order']
    
    all_categories = Categories.objects.filter(parent_category=None)
    all_products = Products.objects.filter()
    categories = Categories.objects.all()
    customer, created = Customer.objects.get_or_create(user=request.user,defaults={'name': request.user.username,'email':request.user.email})
    Wishlistcount = Wishlist.objects.filter(customer=customer).count()

    context = {
        'parent_category':all_categories,
        'categories':categories,
        'all_products' : all_products,
        'items' : product_list,
        'cartTotal' : cartTotal,
        'Wishlistcount' : Wishlistcount,
        'items_count' : product_list.count(),
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
    customer, created = Customer.objects.get_or_create(user=request.user,defaults={'name': request.user.username,'email':request.user.email})
    Wishlistcount = Wishlist.objects.filter(customer=customer).count()
    context = {
        'parent_category':all_categories,
        'categories':categories,
        'all_products' : all_products,
        'items' : items,
        'cartTotal' : cartTotal,
        'Wishlistcount' : Wishlistcount,
        'script' : '/static/js/cartCalc.js',
    }
    return render(request,'cart.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
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
        Wishlistcount = Wishlist.objects.filter(customer = customer).count()

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

def wishlist(request):
    data = cartData(request)
    cartTotal = data['cartItems']
    order = data['order']
    
    all_categories = Categories.objects.filter(parent_category=None)
    all_products = Products.objects.filter()
    categories = Categories.objects.all()
    customer, created = Customer.objects.get_or_create(user=request.user,defaults={'name': request.user.username,'email':request.user.email})
    Wishlistcount = Wishlist.objects.filter(customer=customer).count()
    Wishlistdata = Wishlist.objects.filter(customer=customer)
    context = {
        'parent_category':all_categories,
        'categories':categories,
        'all_products' : all_products,
        'items' : Wishlistdata,
        'cartTotal' : cartTotal,
        'Wishlistcount' : Wishlistcount,

    }
    return render(request,'wishlist.html',context)

def deletewishlist(request,wish_id):
    wishlistItem = Wishlist.objects.filter(id = wish_id).delete()
    return redirect("/store/wishlist")

def deleteCart(request,cart_id):
    wishlistItem = OrderItem.objects.filter(id = cart_id).delete()
    return redirect("/store/cart")

def addtoCartfromwishlist(request,wish_id):
    wishlistItem = Wishlist.objects.get(id = wish_id)
    quantity = int(request.POST.get('quantity',1))
    customer = request.user.customer

    product = Products.objects.get(id=wishlistItem.product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    orderItem.quantity = (orderItem.quantity + quantity)
    
    orderItem.save()
    wishlistItem.delete()
    return redirect("/store/cart")

def clearWishList(request):
    Wishlist.objects.filter(customer = request.user).delete()
    return redirect("/store/wishlist")

def clearCart(request):
    customer = Customer.objects.get(user = request.user)
    order = Order.objects.get(customer = customer, complete = 0) 
    orderItems = OrderItem.objects.filter(order = order).delete()
    return redirect("/store/cart")

def placeOrder(request):
    orderItems = request.POST.getlist('orderItems')
    orderItemsCount = len(orderItems)
    quantity = request.POST.getlist('quantity')
    x = 0
    while(x<=orderItemsCount-1):
        order = OrderItem.objects.filter(id = orderItems[x]).update(quantity = quantity[x])
        x = x+1
    
    for orderItem in orderItems:
        customer = Customer.objects.get(user = request.user)
        order = Order.objects.filter(customer = customer).update(complete = 1)
    
    data={
            'staus' : True,
            'message': 'Order Added, Deliverd by 7 days',
        }

    return JsonResponse(data)