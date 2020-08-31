from django.urls import path
from .views import ( 
    home,
    customer, 
    products
    )

urlpatterns = [
    path('', home),
    path('customer/', customer),
    path('products/', products),

] 