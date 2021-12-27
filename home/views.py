from django.http.response import HttpResponse
from django.shortcuts import render
from administration.models import Categories

from administration.views import categories

# Create your views here.
def index(request):
    all_categories = Categories.objects.filter(parent_category = 1)
    tmp_li = ''
    for cat in all_categories:
        tmp_li = tmp_li+'<li class="sub-mega-menu sub-mega-menu-width-22"><a class="menu-title" href="#">{{cat.cat_name}}</a><ul><li><a href="#">Dresses</a></li><li><a href="#">Blouses & Shirts</a></li><li><a href="#">Hoodies & Sweatshirts</a></li><li><a href="#">Wedding Dresses</a></li><li><a href="#">Prom Dresses</a></li><li><a href="#">Cosplay Costumes</a></li></ul></li>'
    content = {
        'tmp_li':tmp_li
    }
    return render(request,'index.html',content)

def items(request):
    return render(request,'items.html')

def checkout(request):
    return render(request,'checkout.html')

def about(request):
    return render(request,'about.html')
    