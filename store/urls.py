from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('store/items/<int:cat_id>',views.items,name='index'),
    path('store/search/<str:product>',views.productSearch,name='index'),
    path('update_item/', views.updateItem, name="update_item"),
    path('store/cart/', views.cart, name="list cart"),
    path('store/wishlist/', views.wishlist, name="list cart"),
    path('store/deletewishlist/<int:wish_id>', views.deletewishlist, name="delete wish list"),
    path('store/addtoCart/<int:wish_id>', views.addtoCartfromwishlist, name="delete wish list"),
    path('store/clearWishList', views.clearWishList, name="clear WishList"),
    path('addCart/',views.addCart,name='addCart'),
    path('addWishList/', views.addWishList, name="add_wishlist"),
    path('store/deleteCart/<int:cart_id>', views.deleteCart, name="delete cart"),
    path('store/clearCart', views.clearCart, name="clear Cart"),
    path('placeOrder', views.placeOrder, name="placeOrder"),
    
]

