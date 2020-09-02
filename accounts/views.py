from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from .models import *
from .forms import *
def home(request):
    total_orders = Order.objects.all()
    total_customers = Customer.objects.all()
    total_order = total_orders.count()
    delivered = Order.objects.filter(status="Delivered")
    order_deliverd = delivered.count()
    pending = Order.objects.filter(status="Pending")
    order_pending = pending.count()


    context = {
        'total_orders' : total_orders, 'total_customers': total_customers , 'total_order':total_order,
        'order_deliverd':order_deliverd , 'order_pending':order_pending

    }
    return render(request, 'accounts/dashboard.html' , context)

def products(request):
    products = Product.objects.all()
    return render(request ,'accounts/products.html' ,context={'products' : products})


def customer(request , pk):
    try:
        customer = Customer.objects.get(id=pk)

    except Customer.DoesNotExist:
        raise Http404("User Does Not Exist")

    customerorder = customer.order_set.all()
    counter = customerorder.count()
    context = {
        'customer' : customer,'orders':customerorder,'counter':counter
    }
    return render(request,'accounts/customer.html' , context)

def create_order(request , pk):
    customer = Customer.objects.get(id=pk)
    form  = OrderForm(initial={'customer':customer})
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request , 'accounts/order_form.html', context)

def update_order(request , pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request,'accounts/order_form.html',context)
    redirect('/')

def delete_order(request , pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item' : order}
    return render(request, 'accounts/delete.html' , context)

def signin(request):
    context = {}

    return render(request , 'accounts/signin.html',context)

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {'form':form}
    return render(request,'accounts/register.html',context)


