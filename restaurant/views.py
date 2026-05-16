from django.shortcuts import render
from .models import Product

# Create your views here.

def home(request):
    return render(request, 'restaurant/home.html')

def menu(request):
    pizzas = Product.objects.filter(product_type = 'pizza', is_available = True)
    drinks =  Product.objects.filter(product_type = 'drink', is_available = True)
    context = {
        'pizzas':pizzas,
        'drinks':drinks,
    }
    return render(request, 'restaurant/menu.html')

def register(request):
    return render(request, 'restaurant/register.html')