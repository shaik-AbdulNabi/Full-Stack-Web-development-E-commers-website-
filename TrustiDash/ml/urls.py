from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.h,name='h'),
    path('ahome',views.ahome,name='ahome'),
    path('ahome/<int:id>/',views.ahome,name='ahome'),
    path('upload/',views.upload,name='upload'),
    path('upload/<int:id>/',views.upload,name='upload'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('customers/',views.customers,name='customers'),
    path('analatics/',views.analatics,name='analatics'),
   
    
]