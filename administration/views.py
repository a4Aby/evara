from django.db.models import Avg, Max, Min, Sum
from itertools import product
from pickle import FALSE
from statistics import variance
from django.db import connection
from django.http import request
from django.http import HttpResponse,HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render,redirect

from store.models import Order, Wishlist
from .models import Brand, Categories, Color, ProductImages, Products, Size, Variants 
from .forms import CategoryForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect 
from django.contrib.auth import authenticate
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.core import serializers
# Create your views here.

def insertVariants(request):

    product = Products.objects.get(id = request.POST['prd_id'])
    parant = Products.objects.get(id = product.proParent_id)
    

    price = request.POST["prd_price"]
    strike_price = request.POST["prd_strike_price"]
    gst = request.POST["prd_gst"]
    currency = request.POST["prd_currency"]
    width = request.POST["prd_width"]
    height = request.POST["prd_height"]
    weight = request.POST["prd_weight"]
    shipping_fee = request.POST["prd_shipping_fee"]
    availabilityCount = request.POST["prd_availabilityCount"]
    sizeTable = Size.objects.get(name=request.POST["prd_size"])
    


    check = Variants.objects.filter(sizeTable = sizeTable, product= product).count()
    if(check <= 0):
        VariantsItems, created = Variants.objects.get_or_create(
            sizeTable = sizeTable, product= product,availabilityCount = availabilityCount, shipping_fee= shipping_fee,
            weight = weight, height= height,width = width, currency= currency,
            gst = gst, strike_price= strike_price,price= price
        )
    
    lowestVariant = Variants.objects.raw('SELECT * FROM administration_variants WHERE product_id = '+request.POST['prd_id']+' ORDER BY price ASC LIMIT 1')
    for course in lowestVariant:
        prd_price = course.price
        prd_strike_price = course.strike_price
        prd_gst = course.gst
        prd_currency = course.currency
        prd_width = course.width
        prd_height = course.height
        prd_weight = course.weight
        prd_shipping_fee = course.shipping_fee
        prd_size = course.sizeTable.name
        prd_availabilityCount = course.availabilityCount
        prd_sizeTable = Size.objects.get(name=course.sizeTable)
    
        Products.objects.filter(id=request.POST['prd_id']).update(prd_price=prd_price,prd_strike_price=prd_strike_price,prd_gst=prd_gst,
            prd_currency=prd_currency,prd_width=prd_width,prd_height=prd_height,
            prd_weight=prd_weight,prd_shipping_fee=prd_shipping_fee,prd_size=prd_size,
            prd_availabilityCount=prd_availabilityCount,prd_sizeTable=prd_sizeTable,
        )

    lowestChild = Products.objects.raw('select * from administration_products where prd_price > 0 and proParent_id = %s order by prd_price asc limit 1',[product.proParent_id])
    for course in lowestChild:
        prd_price = course.prd_price
        prd_strike_price = course.prd_strike_price
        prd_gst = course.prd_gst
        prd_currency = course.prd_currency
        prd_width = course.prd_width
        prd_height = course.prd_height
        prd_weight = course.prd_weight
        prd_shipping_fee = course.prd_shipping_fee
        prd_size = course.prd_sizeTable.name
        prd_availabilityCount = course.prd_availabilityCount
        prd_sizeTable = Size.objects.get(name=course.prd_sizeTable)
    
        Products.objects.filter(id=product.proParent_id).update(prd_price=prd_price,prd_strike_price=prd_strike_price,prd_gst=prd_gst,
            prd_currency=prd_currency,prd_width=prd_width,prd_height=prd_height,
            prd_weight=prd_weight,prd_shipping_fee=prd_shipping_fee,prd_size=prd_size,
            prd_availabilityCount=prd_availabilityCount,prd_sizeTable=prd_sizeTable,
        )

    return redirect("/add-variant/"+request.POST['prd_id'])

def addVariants(request,parant):

    product = Products.objects.get(id = parant)
    parant = Products.objects.get(id = product.proParent_id)
    variants = Variants.objects.filter(product = product)
    size = Size.objects.all()
    content = {
        'parant' : parant,
        'product' : product,
        'sizes' : size,
        'variants' : variants,
    }

    return render(request,'admin_files/add-new-product-variant.html',content)
    
def showVariants(request):
    parant = request.GET.get('parant', None)
    variance = Products.objects.filter(proParent = parant)
    data = {
        'product' : variance 
    }
    return render(request,'admin_files/variantsList.html',data)

def sizeDelete(request,id):
    record = Size.objects.get(id = id)
    record.delete()
    return redirect("/size-Master")

def sizeAdd(request):
    sizeColor = Size.objects.filter(name = request.POST['name']).count()
    
    if sizeColor == 0:
        AddedSize = Size.objects.create(
                    name = request.POST['name'],
                )
    
    return redirect('/size-Master')

def sizeMaster(request):
    size = Size.objects.all()
    data = {
        'size' : size,
    }
    return render(request,'admin_files/sizeMaster.html', data)

def colorAdd(request):
    checkColor = Color.objects.filter(name = request.POST['name'],code = request.POST['code']).count()
    
    if checkColor == 0:
        AddedColor = Color.objects.create(
                    name = request.POST['name'],
                    code = request.POST['code'],
                )
    
    return redirect('/color-Master')

def colorMaster(request):
    color = Color.objects.all()
    data = {
        'color' : color,
    }
    return render(request,'admin_files/colorMaster.html', data)

def wishList(request):
    wishList = Wishlist.objects.all()
    all_categories = Categories.objects.all()

    data = { 
            'wishList' : wishList,
            'all_categories' : all_categories,
        }
    return render(request,'admin_files/wishList.html', data)



def orderList(request):
    orderList = Order.objects.all()
    all_categories = Categories.objects.all()

    data = { 
            'orderList' : orderList,
            'all_categories' : all_categories,
        }
    return render(request,'admin_files/orderList.html', data)


def get_subcategory(request):
    all_categories = Categories.objects.filter(parent_category=request.POST['mainCategory'])
    jsonData = serializers.serialize('json',all_categories)
    return JsonResponse(jsonData,safe=False)

def brandAdd(request):

    AddedBrand = Brand.objects.create(
                brandName = request.POST['brandName'],
                brandLogo = request.FILES['brandLogo'],
            )
    return redirect('/brand-Master')

def brandMaster(request):
    brand = Brand.objects.all()
    data = {
        'brands' : brand,
    }
    return render(request,'admin_files/brandMaster.html', data)


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
        cat_image = request.FILES["cat_image"]


        if request.POST['parent_category']:
            category = Categories(cat_name=cat_name,cat_slug=cat_slug,parent_category_id=parent_category,cat_description=cat_description,cat_status=cat_status,cat_order=cat_order,cat_image=cat_image)
        else:    
            category = Categories(cat_name=cat_name,cat_slug=cat_slug,cat_description=cat_description,cat_status=cat_status,cat_order=cat_order,cat_image=cat_image)

        category.save()
        return redirect("/administration/categories/")
@login_required
def delete_categories(request,cat_id):
    record = Categories.objects.get(id = cat_id)
    record.delete()
    return redirect("/administration/categories/")


# products
@csrf_protect
@login_required
def add_new_product(request):
    all_categories = Categories.objects.filter(parent_category=None)
    parentProducts = Products.objects.filter(proParent=None)
    brand = Brand.objects.all()
    color = Color.objects.all()
    size = Size.objects.all()
    content = {
        'parent_category':all_categories,
        'products' : parentProducts,
        'brands' : brand,
        'colors' : color,
        'sizes' : size,
    }

    return render(request,'admin_files/add-new-product.html',content)
def updateProduct(request):
    if request.method == "POST":

        prd_sub_category = Categories.objects.get(id=request.POST["prd_sub_category"])
        prd_name = request.POST["prd_name"]
    
        if request.POST['proParent']:
            proParent = Products.objects.get(id=request.POST["proParent"])
    
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
        prd_sub_category = prd_sub_category
        prd_tags = request.POST["prd_tags"]
        prd_is_featured = request.POST.get("is_featured",'0')
        prd_is_popular = request.POST.get("is_popular",'0')
        prd_order =1
        prd_status = 1
        prd_brand = request.POST["prd_brand"]
        prd_color = request.POST["prd_color"]
        prd_size = request.POST["prd_size"]
        prd_availabilityCount = request.POST["prd_availabilityCount"]
        prd_BrandTable = Brand.objects.get(id=request.POST["prd_brand"])
        if request.POST['proParent']:
            update = Products.objects.filter(id=request.POST['id']).update(
                prd_BrandTable=prd_BrandTable,prd_brand=prd_brand,prd_color=prd_color,prd_size=prd_size,prd_availabilityCount=prd_availabilityCount,proParent=proParent,prd_is_featured=prd_is_featured,prd_is_popular=prd_is_popular,prd_name=prd_name,prd_description=prd_description,prd_price=prd_price,prd_strike_price=prd_strike_price,prd_gst=prd_gst,prd_cod_available=prd_cod_available,prd_width=prd_width,prd_height=prd_height,prd_weight=prd_weight,prd_shipping_fee=prd_shipping_fee,prd_currency=prd_currency,prd_image=prd_image,prd_parent_category=prd_parent_category,prd_sub_category=prd_sub_category,prd_tags=prd_tags,prd_order=prd_order,prd_status=prd_status
            )
        else:
            update =Products.objects.filter(id=request.POST['id']).update(
                prd_BrandTable=prd_BrandTable,prd_brand=prd_brand,prd_color=prd_color,prd_size=prd_size,prd_availabilityCount=prd_availabilityCount,prd_is_featured=prd_is_featured,prd_is_popular=prd_is_popular,prd_name=prd_name,prd_description=prd_description,prd_price=prd_price,prd_strike_price=prd_strike_price,prd_gst=prd_gst,prd_cod_available=prd_cod_available,prd_width=prd_width,prd_height=prd_height,prd_weight=prd_weight,prd_shipping_fee=prd_shipping_fee,prd_currency=prd_currency,prd_image=prd_image,prd_parent_category=prd_parent_category,prd_sub_category=prd_sub_category,prd_tags=prd_tags,prd_order=prd_order,prd_status=prd_status
            )

        products_db = Products.objects.get(id=request.POST['id'])
        prd_images = request.FILES.getlist("prd_images")
        
        for image in prd_images:
            Addedimage = ProductImages.objects.create(
                product = products_db,
                image = image,
            )


    return redirect("/product-list/")


def editProduct(request,prd_id):
    product = Products.objects.filter(id = prd_id)
    all_categories = Categories.objects.filter(parent_category=None)
    sub_categories = Categories.objects.filter(parent_category__isnull=False)
    parentProducts = Products.objects.filter(proParent=None)
    brand = Brand.objects.all()
    content = {
        'parent_category':all_categories,
        'products' : parentProducts,
        'brands' : brand,
        'productDet' : product,
        'size' : {"S","M","L","XL","XXL"},
        'gst' : {"5","10","18"},
        'sub_categories' : sub_categories,
    }
    return render(request,'admin_files/edit-product.html',content)


@login_required
def insert_product(request):
    if request.method == "POST":
        prd_description = request.POST["prd_description"]
        prd_image = request.FILES["prd_image"]
        prd_order =1
        prd_status = 1
        prd_brand = request.POST["prd_brand"]
        prd_BrandTable = Brand.objects.get(id=request.POST["prd_brand"])

        if not request.POST['proParent']:
            prd_name = request.POST["prd_name"]
            prd_parent_category = request.POST["prd_parent_category"]
            prd_sub_category = Categories.objects.get(id=request.POST["prd_sub_category"])
            prd_sub_category = prd_sub_category
            prd_tags = request.POST["prd_tags"]
            prd_is_featured = request.POST.get("is_featured",'0')
            prd_is_popular = request.POST.get("is_popular",'0')
            checkP = Products.objects.filter(prd_name = prd_name, prd_parent_category= prd_parent_category, prd_BrandTable= prd_BrandTable,prd_sub_category= prd_sub_category).count()
            if checkP == 0: 
                products_db = Products(prd_BrandTable=prd_BrandTable,prd_brand=prd_brand,prd_is_featured=prd_is_featured,prd_is_popular=prd_is_popular,prd_name=prd_name,prd_description=prd_description,prd_image=prd_image,prd_parent_category=prd_parent_category,prd_sub_category=prd_sub_category,prd_tags=prd_tags,prd_order=prd_order,prd_status=prd_status)
        else:

            proParent = Products.objects.get(id=request.POST["proParent"])
            prd_name = proParent.prd_name
            prd_parent_category = proParent.prd_parent_category
            prd_sub_category = proParent.prd_sub_category
            prd_tags = proParent.prd_tags
            prd_is_featured = proParent.prd_is_featured
            prd_is_popular = proParent.prd_is_popular

            if request.POST.get('prd_cod_available'):
                prd_cod_available = request.POST["prd_cod_available"]
            else:
                prd_cod_available = 0

            prd_color = request.POST["prd_color"]
            prd_colorTable = Color.objects.get(name=request.POST["prd_color"])
            checkP = Products.objects.filter(proParent=proParent,prd_color=prd_color).count()
            if checkP == 0:
                products_db = Products(proParent=proParent,prd_colorTable=prd_colorTable,prd_BrandTable=prd_BrandTable,prd_brand=prd_brand,prd_color=prd_color,prd_is_featured=prd_is_featured,prd_is_popular=prd_is_popular,prd_name=prd_name,prd_description=prd_description,prd_cod_available=prd_cod_available,prd_image=prd_image,prd_parent_category=prd_parent_category,prd_sub_category=prd_sub_category,prd_tags=prd_tags,prd_order=prd_order,prd_status=prd_status)
        
        if checkP == 0:
            products_db.save()
            if request.POST['proParent']:
                prd_images = request.FILES.getlist("prd_images")
                
                for image in prd_images:
                    Addedimage = ProductImages.objects.create(
                        product = products_db,
                        image = image,
                    )
    return redirect("/product-list/")

@login_required
def list_products(request):
    context = {
        'products':Products.objects.filter(proParent=None),
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
