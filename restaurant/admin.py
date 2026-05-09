from django.contrib import admin
from .models import University, User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'email_domain', 'is_active')
    search_fields = ('name', 'email_domain')

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_verified_student', 'university')
    list_filter = ('role', 'is_verified_student', 'university')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra info', {'fields': ('role', 'is_verified_student', 'university')}),
    )