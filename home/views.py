from django.shortcuts import render
from products.models import Product, SubCategory, Category, Review
from glacial_ac.views import get_subcat
nav_subcat = get_subcat()
# Create your views here.


def index(request):
    """ A view to reneder index page"""
    products = Product.objects.all().order_by('-id')[:4]

    context = {
        'products' : products,
        'nav_subcat' : nav_subcat,
    }

    return render(request, 'home/index.html', context)
