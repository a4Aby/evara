from django import forms
from django.db.models import fields
from django.forms import ModelForm
from .models import Categories


# create form

class CategoryForm(ModelForm):
    class Meta:
        model = Categories
        fields = '__all__' # ('name','bla ','..')