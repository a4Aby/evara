from django.db import connection
from django.http import request
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from .models import Categories, Products
from .forms import CategoryForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect 
from django.contrib.auth import authenticate
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
# Create your views here.
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return redirect("/administration/")
        else:
            messages.success(request,'Ther was an error login')
            return render(request,'admin_files/login.html')
    else:
        return render(request,'admin_files/login.html')

@login_required
def dashboard(request):
    return render(request,'admin_files/index.html')

@login_required
def categories(request):
        all_categories = Categories.objects.all()
        data = { 
            'all_categories' : all_categories,
            'i' : 0
        }
        return render(request,'admin_files/categories.html',{"all_categories" : data})
@login_required
def add_categories(request):
    if request.method == "POST":
        cat_name = request.POST['cat_name']
        cat_slug = request.POST['cat_slug']
        parent_category = request.POST['parent_category']
        cat_description = request.POST['cat_description']
        cat_status = 1
        cat_order = 1
        if request.POST['parent_category']:
            category = Categories(cat_name=cat_name,cat_slug=cat_slug,parent_category_id=parent_category,cat_description=cat_description,cat_status=cat_status,cat_order=cat_order)
        else:    
            category = Categories(cat_name=cat_name,cat_slug=cat_slug,cat_description=cat_description,cat_status=cat_status,cat_order=cat_order)

        category.save()
        return redirect("/administration/categories/")
@login_required
def delete_categories(request,cat_id):
    record = Categories.objects.get(id = cat_id)
    record.delete()
    return redirect("/administration/categories/")

def get_subcategory(request):

    all_categories = Categories.objects.filter(parent_category=request.POST['mainCategory'])
    return HttpResponse(all_categories, mimetype="text/json")

# products
@csrf_protect
@login_required
def add_new_product(request):
    all_categories = Categories.objects.filter(parent_category=None)
    
    content = {
        'parent_category':all_categories,
    }

    return render(request,'admin_files/add-new-product.html',content)

@login_required
def insert_product(request):
    if request.method == "POST":
        prd_name = request.POST["prd_name"]
        prd_description = request.POST["prd_description"]
        prd_price = request.POST["prd_price"]
        prd_strike_price = request.POST["prd_strike_price"]
        prd_currency = request.POST["prd_currency"]
        prd_gst = request.POST["prd_gst"]
        prd_cod_available = request.POST["prd_cod_available"]
        prd_width = request.POST["prd_width"]
        prd_height = request.POST["prd_height"]
        prd_weight = request.POST["prd_weight"]
        prd_shipping_fee = request.POST["prd_shipping_fee"]
        prd_image = request.FILES["prd_image"]
        prd_parent_category = request.POST["prd_parent_category"]
        prd_sub_category = request.POST["prd_sub_category"]
        prd_tags = request.POST["prd_tags"]
        prd_order =1
        prd_status = 1
        products_db = Products(prd_name=prd_name,prd_description=prd_description,prd_price=prd_price,prd_strike_price=prd_strike_price,prd_gst=prd_gst,prd_cod_available=prd_cod_available,prd_width=prd_width,prd_height=prd_height,prd_weight=prd_weight,prd_shipping_fee=prd_shipping_fee,prd_currency=prd_currency,prd_image=prd_image,prd_parent_category=prd_parent_category,prd_sub_category=prd_sub_category,prd_tags=prd_tags,prd_order=prd_order,prd_status=prd_status)
        products_db.save()
    return redirect("/list-product/")

@login_required
def list_products(request):
    context = {
        'products':Products.objects.all(),
    } 
    return render(request,'admin_files/product-list.html',context)
    
#form
@login_required
def add_category_form(request):
    all_categories = Categories.objects.all()
    submitted = False
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_category_form?submitted=True')
    else:
        form = CategoryForm
        if 'submitted' in request.GET:
            submitted = True
    data = { 
        'all_categories' : all_categories,
        'i' : 0,
        'form' : form,
        'submitted' : submitted
    }
    return render(request,'add_categories_form.html',data)
