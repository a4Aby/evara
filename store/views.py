from django.http.response import HttpResponse
from django.shortcuts import render
from administration.models import Categories
from administration.models import Products
from django.http import JsonResponse
import json
from .models import * 

# Create your views here.

def items(request,cat_id):
    items = Products.objects.filter(prd_sub_category = cat_id)
    cartTotal = Order.get_cart_total
    context = {
        'items' : items,
        'cartTotal' : cartTotal,
    }
    return render(request,'store.html',context)

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
