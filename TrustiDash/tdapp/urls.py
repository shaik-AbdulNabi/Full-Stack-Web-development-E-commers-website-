from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.p,name='p'),
    path('uhome',views.uhome,name='uhome'),
    
    path('buy_items/', views.buy_items, name='buy_items'),
    

    path('delete/<int:id>/',views.delete,name='delete'),
    path('cproductdelete/<int:id>/',views.cproductdelete,name='cproductdelete'),
    path('cartadd/<int:id>/',views.cartadd,name='cartadd'),   
    path('wishlistadd/<int:id>/',views.wishlistadd,name='wishlistadd'),   
    path('cart',views.cart,name='cart'),
    path('wishlist',views.wishlist,name='wishlist'),
    path('wproductdelete/<int:id>/',views.wproductdelete,name='wproductdelete'),
   

   
    
]