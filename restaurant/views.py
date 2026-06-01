from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Product, ProductSize, Topping, PizzaTopping, ToppingSizePrice, Order, OrderItem, OrderItemTopping
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


def pizza_detail(request, pizza_id):
    pizza = get_object_or_404(Product, id=pizza_id, product_type='pizza', is_available=True)
    sizes = ProductSize.objects.filter(product=pizza).select_related('size')
    allowed_toppings = PizzaTopping.objects.filter(product=pizza).select_related('topping')

    context = {
        'pizza': pizza,
        'sizes': sizes,
        'allowed_toppings': allowed_toppings,
    }
    return render(request, 'restaurant/pizza_detail.html', context)

@login_required
def add_to_cart(request):
    if request.method != 'POST':
        return redirect('menu')
    
    product_size_id = request.POST.get('product_size_id')
    topping_ids = request.POST.getlist('toppings')

    product_size = get_object_or_404(ProductSize, id=product_size_id)

    order, created = Order.objects.get_or_create(
        user = request.user, status = 'in_basket', defaults = {'total_price': 0, 'discount_applied': 0}
    )

    item_price = product_size.base_price
    selected_toppings = []
    for topping_id in topping_ids:
        try: 
            topping_price_obj = ToppingSizePrice.objects.get(
                topping_id = topping_id,
                size = product_size.size
            )
            item_price += topping_price_obj.price
            selected_toppings.append((topping_price_obj.topping, topping_price_obj.price))

        except ToppingSizePrice.DoesNotExist:
            pass


    order_item = OrderItem.objects.create(
        order = order,
        product_size = product_size,
        quantity = 1,
        item_total_price = item_price
    )

    for topping, price in selected_toppings:
        OrderItemTopping.objects.create(
            order_item = order_item,
            topping = topping,
            topping_price = price
        )
    
    messages.success(request, f'{product_size.product.name} ({product_size.size.name}) added to your cart!')
    return redirect('cart')


@login_required
def cart(request):
    try:
        order = Order.objects.get(user=request.user, status='in_basket')
        items = order.items.all().select_related('product_size__product', 'product_size__size')

        total = sum(item.item_total_price for item in items)
        order.total_price = total
        order.save()

    except Order.DoesNotExist:
        order = None
        items = []
        total = 0

    context = {
        'order': order,
        'items': items,
        'total': total,
    }
    return render(request, 'restaurant/cart.html', context)

@login_required
def checkout(request):
    try:
        order = Order.objects.get(user=request.user, status='in_basket')
    except Order.DoesNotExist:
        messages.error(request, 'Your cart is empty.')
        return redirect('menu')

    items = order.items.all().select_related('product_size__product', 'product_size__size')
    subtotal = sum(item.item_total_price for item in items)

    discount = 0
    if request.user.is_verified_student:
        discount = round(subtotal * 10 / 100, 2)

    total = subtotal - discount

    if request.method == 'POST':
        order.status = 'ordered'
        order.total_price = total
        order.discount_applied = discount
        order.save()

        has_pizza = any(item.product_size.product.product_type == 'pizza' for item in items)
        if has_pizza:
            from .models import LoyaltyProgram, UserLoyalty
            try:
                program = LoyaltyProgram.objects.first()
                if program:
                    user_loyalty, _ = UserLoyalty.objects.get_or_create(
                        user=request.user, program=program
                    )
                    user_loyalty.stamp_count += 1
                    user_loyalty.save()
                    order.loyalty_counted = True
                    order.save()
            except Exception:
                pass

        messages.success(request, 'Your order has been placed successfully!')
        return redirect('order_history')

    context = {
        'order': order,
        'items': items,
        'subtotal': subtotal,
        'discount': discount,
        'total': total,
    }
    return render(request, 'restaurant/checkout.html', context)


@login_required
def remove_from_cart(request, item_id):
    order_item = get_object_or_404(OrderItem, id = item_id, order__user = request.user)
    order_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')

@login_required
def order_history(request):
    orders = Order.objects.filter(user = request.user).exclude(status = 'in_basket').order_by('-order_date')
    context = {
        'orders': orders,
    }
    return render(request, 'restaurant/order_history.html', context)