from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_subcategory/', views.add_subcategory, name='add_subcategory'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist,
         name='add_to_wishlist'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product,
         name='delete_product'),
    path('submit_review/<int:product_id>/', views.submit_review,
         name='submit_review'),


]
