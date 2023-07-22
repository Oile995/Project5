from django.contrib import admin
from .models import Product, Category, SubCategory


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('friendly_name', 'name',)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'friendly_name', 'name',)



class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'subcategory',
        'price',
        'rating',
        'image',
    )
    

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)