from django.contrib import admin
from .models import Product, Category, SubCategory, Review
from django_summernote.admin import SummernoteModelAdmin


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('friendly_name', 'name',)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'friendly_name', 'name',)


class ProductAdmin(SummernoteModelAdmin):
    summernote_fields = ('description', 'specification')
    list_display = (
        'name',
        'sku',
        'subcategory',
        'price',
        'rating',
        'image',
    )
    search_fields = ['name', 'subcategory', 'active_deal']
    list_filter = ('name', 'subcategory')


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