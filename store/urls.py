from django.urls import path

from . import views

urlpatterns = [
    path('store/items/<int:cat_id>',views.items,name='index'),
    path('update_item/', views.updateItem, name="update_item"),
    path('store/cart/', views.cart, name="list cart"),
]

