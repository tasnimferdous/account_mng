from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only
# Create your views here.

@unauthenticated_user
def registration(request): 
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account is created for '+ username)
            return redirect('login')
    context = {'form':form}
    return render(request, 'accounts/registration.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is Incorrect')
    context = {}
    return render(request, 'accounts/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance = customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance = customer)
        if form.is_valid:
            form.save()
    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = len(orders)
    orders_delivered = orders.filter(status = 'Delivered').count()
    orders_pending = orders.filter(status  = 'Pending').count()
    context = {'orders':orders,'total_orders':total_orders,
                'orders_delivered':orders_delivered,
                'orders_pending':orders_pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url = 'login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_customers = customers.count()
    total_orders = len(orders)
    orders_delivered = orders.filter(status = 'Delivered').count()
    orders_pending = orders.filter(status  = 'Pending').count()
    context = {'customers':customers,'orders':orders,
                'total_orders':total_orders,
                'orders_delivered':orders_delivered,
                'orders_pending':orders_pending
                }
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products':products})


# Information of a customer and his orders
@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def customer(request,customer_id):
    customer = Customer.objects.get(id = customer_id)
    orders = customer.order_set.all()
    order_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset = orders)
    orders = myFilter.qs

    context = {'customer':customer,'orders':orders,'order_count':order_count, 'myFilter':myFilter}
    return render(request, 'accounts/customer.html',context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def createOrder(request, customer_id):
    OrderFormSet = inlineformset_factory(Customer, Order, fields = ('product','status'), extra = 5)
    customer = Customer.objects.get(id = customer_id)
    formset = OrderFormSet(queryset = Order.objects.none() ,instance = customer)
    # form = OrderForm(initial = {'customer':customer})
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST ,instance = customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render(request, 'accounts/create_order.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def updateOrder(request, order_id):
    order = Order.objects.get(id = order_id)
    form = OrderForm(instance = order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance = order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request,'accounts/create_order.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def deleteOrder(request, order_id):
    order = Order.objects.get(id = order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request,'accounts/delete_order.html', context)
