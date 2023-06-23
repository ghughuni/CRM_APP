from django.urls import path
from .views import (
    index,
    home,
    logout_view,
    register,
    customer_record,
    customer_delete,
    add_customer
    )

urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('logout_view/', logout_view, name='logout_view'),
    path('record/<str:pk>', customer_record, name='record'),
    path('customer_delete/<str:pk>', customer_delete, name='customer_delete'),
    path('add_customer/', add_customer, name='add_customer'),


]
