from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stock/<int:pk>', views.stock_detail, name='stock_detail'),
    path('delete_stock/<int:pk>', views.delete_stock, name='delete_stock'),
]