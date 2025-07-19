from django.contrib import admin
from .models import ProductCategory,Product,Cart,CartItem
from .models import SellerApplication

@admin.register(ProductCategory)
class categoryAdmin(admin.ModelAdmin):
    list_display = ('name','description','created_at')


class productAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','seller','location')

admin.site.register(SellerApplication)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Product,productAdmin)
