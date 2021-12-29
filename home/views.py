from django.http.response import HttpResponse
from django.shortcuts import render
from administration.models import Categories

from administration.views import categories

# Create your views here.
def index(request):
    all_categories = Categories.objects.filter(parent_category=None)
    categories = Categories.objects.all()
    content = {
        'parent_category':all_categories,
        'categories':categories
    }
    print(content)
    return render(request,'index.html',content)

def items(request):
    return render(request,'items.html')

def checkout(request):
    return render(request,'checkout.html')

def about(request):
    return render(request,'about.html')
    