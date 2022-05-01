from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('',views.index,name="home"),
    path('handleLogin',views.handleLogin,name="handleLogin"),
    path('handleLogout',views.handleLogout,name="handleLogout"),
    path('signup',views.signup,name="signup"),
    path('add_product',views.add_product,name="add_product"),
    path('seller',views.seller,name="seller"),
    path('customer',views.customer,name="customer"),

    path('delivery',views.delivery,name="delivery"),

    path('electronics', views.electronics, name='electronics'),
    path('groceries', views.groceries, name='groceries'),
    path('clothing', views.clothing, name='clothing'),
    path('checkout', views.checkout, name='checkout'),

    path('update_item', views.update_item, name='update_item'),
    path('create_order', views.create_order, name='create_order'),
    path('your_orders', views.your_orders, name='your_orders'),
    path('your_orders/<int:orderID>', views.order)
]
