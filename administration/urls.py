from django.urls import path

from . import views

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
    
]