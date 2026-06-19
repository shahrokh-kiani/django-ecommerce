from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/toggle/', views.order_toggle_status, name='order_toggle_status'),
]