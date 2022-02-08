from django.urls import path

from . import views

app_name = 'dj_razorpay'

urlpatterns = [
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('payment_load/', views.payment_load, name='payment_load')
]

