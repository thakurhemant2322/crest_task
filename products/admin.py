from django.contrib import admin
from .models import Product, ProductLog

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','title','price','is_active','created_on','updated_on')
    list_filter = ('is_active',)
    search_fields = ('title','description','ssn')

@admin.register(ProductLog)
class ProductLogAdmin(admin.ModelAdmin):
    list_display = ('id','product','action','at')
    list_filter = ('action',)
