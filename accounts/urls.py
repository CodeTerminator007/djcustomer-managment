from django.urls import path
from .views import *

urlpatterns = [
    path('', home , name="home"),
    path('customer/<int:pk>', customer , name="customer"),
    path('products/', products , name="products"),
    path('logout/', logoutuser , name="logout"),
    path('create_order/<str:pk>',create_order, name="create_order"),
    path('update_order/<str:pk>',update_order, name="update_order"),
    path('delete_order/<str:pk>',delete_order, name="delete_order"),
    path('login/',signin ,name='signin'),
    path('register/' , register , name="register"),
    path('user/' , userPage , name="user-page"),
    path('settings/',settings_user , name='user_settings')


] 