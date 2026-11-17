from django.contrib import admin
from .models import Product, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock')
    list_filter = ('category',)
    search_fields = ('name', 'category')
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'full_name',
        'total_amount',
        'status',
        'created_at',
    )
    fields = (
    'user',
    'full_name',
    'address',
    'phone',
    'total_amount',
    'status',
    'created_at',
)
    readonly_fields = ('user', 'created_at')

    list_filter = ('status', 'created_at')

    search_fields = (
        'full_name',
        'user__username',
        'phone',
    )

    ordering = ('-created_at',)