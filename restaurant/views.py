from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .models import Product
from .forms import RegisterForm

# Create your views here.

def home(request):
    return render(request, 'restaurant/home.html')

def menu(request):
    pizzas = Product.objects.filter(product_type = 'pizza', is_available = True)
    drinks =  Product.objects.filter(product_type = 'drink', is_available = True)
    print("PIZZAS:", pizzas)
    print("DRINKS:", drinks)
    context = {
        'pizzas':pizzas,
        'drinks':drinks,
    }
    return render(request, 'restaurant/menu.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Registration successful. Welcome, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'restaurant/register.html', {'form': form})