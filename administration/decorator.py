from django.http import HttpResponse
from django.shortcuts import redirect

def check_access_permission(view_func):
    def wrapper_func(request,*args,**kwargs):
        return HttpResponse(request.user)
        return True