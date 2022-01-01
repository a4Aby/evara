from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('items/',views.items,name='index'),
    path('checkout/',views.checkout,name='index'),
    path('item-detail/',views.items,name='index'),
    # path('login/',views.items,name='index'),
    path('store/',views.items,name='index'),
    path('about/',views.about,name='about us'),
]
