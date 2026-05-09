from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=200, unique = True)
    email_domain = models.CharField(max_length=100, unique = True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Universities'

    def __str__(self):
        return self.name
    

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('staff', 'Staff'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default = 'customer')
    is_verified_student = models.BooleanField(default=False)
    university = models.ForeignKey(
        University, 
        on_delete=models.SET_NULL, 
        null=True, blank = True
    )
    def __str__(self):
        return self.username
    

class Product(models.Model):
    PRODUCT_TYPES = (
        ('pizza', 'Pizza'),
        ('drink', 'Drink'),
    )
    name = models.CharField(max_length=200, unique = True)
    description = models.TextField(blank = True)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class Size(models.Model):
    name = models.CharField(max_length=50, unique = True)
    description = models.TextField(max_length=200, blank = True)
    size_type = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    base_price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('product', 'size')

    def __str__(self):
        return f"{self.product.name} - {self.size.name}"
    

class Allergen(models.Model):
    name = models.CharField(max_length=100, unique = True)

    def __str__(self):
        return self.name
    

class ProductAllergen(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    allergen = models.ForeignKey(Allergen, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'allergen')

    def __str__(self):
        return f"{self.product.name} - {self.allergen.name}"
    

class Topping(models.Model):
    name = models.CharField(max_length=100, unique = True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class ToppingAllergen(models.Model):
    topping = models.ForeignKey(Topping, on_delete=models.CASCADE)
    allergen = models.ForeignKey(Allergen, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('topping', 'allergen')

    def __str__(self):
        return f"{self.topping.name} - {self.allergen.name}"
    

class PizzaTopping(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    topping = models.ForeignKey(Topping, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'topping')

    def __str__(self):
        return f"{self.product.name} - {self.topping.name}"
    

class ToppingSizePrice(models.Model):
    topping = models.ForeignKey(Topping, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('topping', 'size')

    def __str__(self):
        return f"{self.topping.name} - {self.size.name} - {self.price}"
    

class LoyaltyProgram(models.Model):
    PROGRAM_TYPES = (
        ('pizza_only', 'Pizza Only'), 
        ('pizza_and_drink', 'Pizza and Drink'),
    )
    name = models.CharField(max_length=100, unique = True)
    program_type = models.CharField(max_length=20, choices=PROGRAM_TYPES)
    stamps_required = models.IntegerField(default=8)
    discount_pct = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name
    
class UserLoyalty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(LoyaltyProgram, on_delete=models.CASCADE)
    stamp_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'program')

    def __str__(self):
        return f"{self.user.username} - {self.program.name}: {self.stamp_count} stamps"
    

class Order(models.Model):
    STATUS_CHOICES = (
        ('in_basket', 'In Basket'),
        ('ordered', 'Ordered'),
        ('preparing', 'Preparing'),
        ('ready_for_pickup', 'Ready for Pickup'),
        ('completed', 'Completed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loyalty_program = models.ForeignKey(LoyaltyProgram, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_basket')
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    discount_applied = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    loyalty_counted = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} - {self.status}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_size = models.ForeignKey(ProductSize, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    item_total_price = models.DecimalField(max_digits=8, decimal_places=2)
    

    def __str__(self):
        return f"{self.quantity} x {self.product_size.product.name}"
    

class OrderItemTopping(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    topping = models.ForeignKey(Topping, on_delete=models.PROTECT)
    topping_price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta: 
        unique_together = ('order_item', 'topping')

    def __str__(self):
        return f"{self.order_item} - {self.topping.name}"