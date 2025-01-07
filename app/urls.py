from django.contrib import admin
from django.urls import path,include
from .views import *
from . import admin_views
urlpatterns = [
    path('',home),
    path('accounts/profile/',profile),

    path('post/add/',new_post),
    path('post/edit/<id>/',editpost),
    path('post/delete/<id>/',deletepost),
    path('post/view/<id>/',view_post),
    path('post/all/',user_posts),
    path('post/orders/',user_orders),
    path('post/order/update/confirm/<id>/',user_orders_confirm),
    path('post/order/update/cancel/<id>/',user_orders_cancel),
    path('post/order/update/<id>/',user_orders_update),
    path('post/profile/<id>/',post_profile),
    path('post/reviews/',post_reviews),
    path('profile/reviews/',profile_reviews),

    path('search/',search),

    #orders
    path('orders',orders),
    path('order/<str:id>',orderdetails),
    path('order/<int:id>/<int:q>/',makeorder),
    path('order/cancel/<int:id>',cancelorder),
    path('order/return/<int:id>',returnorder),
    path('order/payment/<str:id>/',orderpayment),
    
    path('order/payment/success/<str:pay>/<str:id>',paysuccess),
    path('order/payment/failed/<str:pay>/<str:id>',payfailed),

    #admin
    path('admin/',admin_views.dashboard),
    path('admin/category/',admin_views.category),
    path('admin/category/edit/<id>/',admin_views.category_edit),
    path('admin/category/delete/<id>/',admin_views.category_delete),
    path('admin/slider/',admin_views.slider),
    path('admin/slider/edit/<id>/',admin_views.slider_edit),
    path('admin/slider/delete/<id>/',admin_views.slider_delete),
    path('admin/reviews',admin_views.reviews),
    path('admin/review/delete/<id>/',admin_views.review_delete),

    path('admin/transactions/',admin_views.transactions),
    path('admin/users/',admin_views.users),

    #orders
    path('admin/orders/',admin_views.orders),
    path('admin/order/update/<int:id>/',admin_views.updateorder),
]