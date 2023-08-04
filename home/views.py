from django.shortcuts import render
from products.models import Product, SubCategory, Category, Review


def index(request):
    """ A view to reneder index page"""
    products = Product.objects.all().order_by('-id')[:4]

    context = {
        'products': products,
    }
    return render(request, 'home/index.html', context)
