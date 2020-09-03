from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import login , logout 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate
from django.contrib.auth.models import User ,Group 
from .decorators import *
from .models import *
from .forms import *


@login_required(login_url='signin')
@admin_only
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


@login_required(login_url='signin')
@allowed_user(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request ,'accounts/products.html' ,context={'products' : products})

@allowed_user(allowed_roles=['admin'])
def customer(request , pk ):
    try:
        customer = Customer.objects.get(id=pk)
        user = User.objects.get(id=pk)

    except User.DoesNotExist:
        raise Http404("User Does Not Exist")
    
    customerorder = customer.order_set.all()
    userorder = user.order_set.all()
    userordercount = userorder.count()

    counter = customerorder.count()
    context = {
        'customer' : customer,'orders':customerorder,'counter':counter , 'userorder': userorder , 'userordercount':userordercount
    }
    return render(request,'accounts/customer.html' , context)


@login_required(login_url='signin')
@allowed_user(allowed_roles=['admin'])
def create_order(request , pk):
    customer = Customer.objects.get(id=pk)
    form  = OrderForm(initial={'user':customer})
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request , 'accounts/order_form.html', context)

@login_required(login_url='signin')
@allowed_user(allowed_roles=['admin'])
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

@login_required(login_url='signin')
@allowed_user(allowed_roles=['admin'])
def delete_order(request , pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item' : order}
    return render(request, 'accounts/delete.html' , context)


@unauthenticated_user
def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request , username=username, password=password)
        if user is not None:
            login(request,user)
            group = None

            if user.groups.exists():
                group = user.groups.all()[0].name

            if group == 'customer':
                return redirect('user-page')
            if group == 'admin':
                return redirect('home')

        else:
            messages.info(request, 'Three credits remain in your account.')

    context = {}

    return render(request , 'accounts/signin.html',context)


@unauthenticated_user
def register(request):  
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            Customer.objects.create(user=user)            
            user.groups.add(group)
            return redirect("/")

    context = {'form':form}
    return render(request,'accounts/register.html',context)
 
def logoutuser(request):
    logout(request)

    context ={}

    return redirect('signin')

@login_required(login_url='signin')
@allowed_user(allowed_roles=['customer'])
def userPage(request):
    orders =request.user.customer.order_set.all()
    context = {'orders': orders}

    return render(request , 'accounts/user.html' , context)


def settings_user(request):
    customer = request.user.customer
    form =  CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
            
    context = {'form' : form }

    return render(request , 'accounts/settings_update.html' , context)