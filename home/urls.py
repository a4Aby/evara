from turtle import home
from django.urls import path

from . import views
app_name = 'home'
urlpatterns = [
    path('',views.index,name='index'),
    path('items/',views.items,name='index'),
    path('checkout/',views.checkout,name='index'),
    path('item-detail/',views.items,name='index'),
    # path('login/',views.items,name='index'),
    path('store/',views.items,name='index'),
    path('about/',views.about,name='about us'),
    path('itemlist/',views.itemList,name='itmeList'),
    path('productDetials/',views.productDetials,name='productDetials'),
    path('childproductDetials/',views.childproductDetials,name='childproductDetials'),
    path('productVariants/',views.productVariants,name='productVariants'),
]
