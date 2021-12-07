from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact),
    path('product-plus/', views.product_plus),
    path('product-plus-list/', views.product_plus_list, name='product_plus_list'),
    path('new-product/', views.create_product),
    path('products/', views.product_list, name='product_list'),
    path('update-product/<str:pk>', views.product_update, name='product_update')
]
