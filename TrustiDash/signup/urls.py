from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('s',views.s,name='s'),
    path('',views.main,name=''),
           
    path('forgot_password/',views.forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
    path('login/',views.sinoutf,name='login'),
    path('logout/',views.logout,name='logout'),
    
   
    
]