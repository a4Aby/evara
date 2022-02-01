from tokenize import group
from django.http import HttpResponse
from django.shortcuts import redirect

def check_access_permission(view_func):
    def wrapper_func(request,*args,**kwargs):
        return HttpResponse(request.user)
        return True

def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            group = None

            for g in request.user.groups.all():
                group = g.name

            # if request.users.groups.exists():
            #     group = request.users.groups.all()
            print('group ',group)
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator
        