from django.urls import path

from . import views

app_name = 'administration'

urlpatterns = [
    path('login/',views.login,name='login'),
    path('administration/',views.dashboard,name='dashboard'),
    path('administration/categories/',views.categories,name='categories'),
    path('administration/add_categories/',views.add_categories,name='add categories'),
    path('delete-categories/<int:cat_id>',views.delete_categories,name='delete categories'),
    path('add-new-product/',views.add_new_product,name='add new product'),
    path('insert-product/',views.insert_product,name='insert product'),
    path('product-list/',views.list_products,name='product list'),
    path('add_category_form/',views.add_category_form,name="add category using form"),
    path('get_subcategory',views.get_subcategory,name="get_subcategory"),
    path('order-list',views.orderList,name="orderList"),
    path('wish-list',views.wishList,name="wishList"),
    path('brand-Master',views.brandMaster,name="brandMaster"),
    path('add_brand',views.brandAdd,name="add brand from admin"),
    path('editProduct/<int:prd_id>',views.editProduct,name="edit brand from admin"),
    path('edit-product',views.updateProduct,name="update brand from admin"),
    path('color-Master',views.colorMaster,name="colorMaster"),
    path('add_color',views.colorAdd,name="add color from admin"),
    path('size-Master',views.sizeMaster,name="sizeMaster"),
    path('add_size',views.sizeAdd,name="add brand from admin"),
    path('delete-size/<int:id>',views.sizeDelete,name="delete size"),
    path('showVariants',views.showVariants,name='showVariants'),
    path('add-variant/<int:parant>',views.addVariants,name="showVariants"),
    path('insertVariants',views.insertVariants,name="insertVariants"),
    path('addToShip',views.addToShip,name="addToShip"),
]