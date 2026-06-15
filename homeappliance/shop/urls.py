from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_main_page, name='shop_main_page'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/rate/', views.submit_rating, name='submit_rating'),
    path('category/<int:pk>/', views.category_page, name='category_page'),
]