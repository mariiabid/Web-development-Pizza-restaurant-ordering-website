from django.contrib import admin
from .models import University, User, Product, Size, ProductSize, Allergen, ProductAllergen, Topping, ToppingAllergen, PizzaTopping, ToppingSizePrice, LoyaltyProgram, UserLoyalty, Order, OrderItem, OrderItemTopping
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['name', 'email_domain', 'is_active']
    search_fields = ['name', 'email_domain']

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_verified_student', 'university']
    list_filter = ['role', 'is_verified_student', 'university']
    fieldsets = UserAdmin.fieldsets + (
        ('Extra info', {'fields': ['role', 'is_verified_student', 'university']}),
    )

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 3

class ProductAllergenInline(admin.TabularInline):
    model = ProductAllergen
    extra = 1

class PizzaToppingInline(admin.TabularInline):
    model = PizzaTopping
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_type','diet_info','is_available']
    list_filter = ['product_type','diet_info','is_available']
    search_fields = ['name']
    inlines = [ProductSizeInline, ProductAllergenInline, PizzaToppingInline]

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'size_type']

class ToppingAllergenInline(admin.TabularInline):
    model = ToppingAllergen
    extra = 1

class ToppingSizePriceInline(admin.TabularInline):
    model = ToppingSizePrice
    extra = 3

@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_available']
    inlines = [ToppingAllergenInline, ToppingSizePriceInline]


@admin.register(Allergen)
class AllergenAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(LoyaltyProgram)
class LoyaltyProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'program_type', 'stamps_required', 'discount_pct']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'order_date', 'total_price', 'discount_applied']
    list_filter = ['status']
    search_fields = ['user__username']

class OrderItemToppingInline(admin.TabularInline):
    model = OrderItemTopping
    extra = 0

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_size', 'quantity', 'item_total_price']
    inlines = [OrderItemToppingInline]