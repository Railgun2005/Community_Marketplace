from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .models import Category,UserProfile,Item,Order
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm,OrderForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.http import urlencode,url_has_allowed_host_and_scheme
from django.db.models import Sum, F

def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,("Registration Successful"))
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,("Login Successful"))
            return redirect('home')
        else:
            messages.success(request,("Login Failed"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

@login_required
def logout_user(request):
    logout(request)
    messages.success(request,("Logout Successful"))
    return redirect('home')

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES, 
                                   instance=user_profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=user_profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_profile': user_profile
    }
    return render(request, 'profile.html', context)

def home(request):
    active_traders = User.objects.filter(order__isnull=False).distinct().count()
    active_orders = Order.objects.count()
    turnover_agg = Order.objects.aggregate(total_turnover=Sum(F('price') * F('quantity')))
    current_turnover = turnover_agg['total_turnover'] or 0
    context = {
        'active_traders': active_traders,
        'active_orders': active_orders,
        'current_turnover': current_turnover,
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html', {})

@login_required
def dashboard(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-date')
    buy_orders = user_orders.filter(order_type=True)   
    sell_orders = user_orders.filter(order_type=False)  
    context = {
        'buy_orders': buy_orders,
        'sell_orders': sell_orders,
    }
    return render(request, 'dashboard.html', context)

@login_required
def market(request):
    categories = Category.objects.all()
    selected_category_id = request.GET.get('category_id')
    selected_item_id = request.GET.get('item_id')
    items = []
    if selected_category_id:
        items = Item.objects.filter(category_id=selected_category_id)
    selected_item = None
    buy_orders = []
    sell_orders = []
    if selected_item_id:
        selected_item = Item.objects.get(id=selected_item_id)
        orders = Order.objects.filter(item=selected_item)
        buy_orders = orders.filter(order_type=True)
        sell_orders = orders.filter(order_type=False)
    context = {
        'categories': categories,
        'items': items,
        'selected_category_id': int(selected_category_id) if selected_category_id else None,
        'selected_item': selected_item,
        'buy_orders': buy_orders,
        'sell_orders': sell_orders,
    }
    return render(request, 'market.html', context)

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            messages.success(request, 'Order created successfully!')
            redirect_url = get_redirect_url(request)
            return redirect(redirect_url)
    else:
        initial_data = {}
        if hasattr(request.user, 'userprofile'):
            initial_data['location'] = request.user.userprofile.address
            initial_data['phone'] = request.user.userprofile.phone
        form = OrderForm(initial=initial_data)
    return render(request, 'order_form.html', {
        'form': form,
        'title': 'Create New Order'
    })

@login_required
def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order updated successfully!')
            redirect_url = get_redirect_url(request)
            return redirect(redirect_url)
    else:
        form = OrderForm(instance=order)
    context = {
        'form': form,
        'title': 'Update Order',
        'category_id': request.GET.get('category_id'),
        'item_id': request.GET.get('item_id')
    }
    return render(request, 'order_form.html', context)

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Order deleted successfully!')
        redirect_url = get_redirect_url(request)
        return redirect(redirect_url)
    context = {
        'order': order,
        'category_id': request.GET.get('category_id'),
        'item_id': request.GET.get('item_id')
    }
    return render(request, 'confirm_delete.html', context)

@login_required
def get_redirect_url(request, default_view='dashboard'):
    category_id = request.POST.get('category_id') or request.GET.get('category_id')
    item_id = request.POST.get('item_id') or request.GET.get('item_id')
    next_url = request.POST.get('next') or request.GET.get('next')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return next_url
    elif category_id and item_id:
        market_url = reverse('market')
        params = urlencode({'category_id': category_id, 'item_id': item_id})
        return f"{market_url}?{params}"
    else:
        return reverse(default_view)