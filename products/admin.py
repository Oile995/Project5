from django.contrib import admin
from .models import Product, Category, SubCategory, Review


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

class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'rating',
        'user',
        'created_on',
    )
    

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)