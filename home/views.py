from django.shortcuts import render
from products.models import Product

# Create your views here.

def index(request):
    """ A view to reneder index page"""

    products = Product.objects.filter(active_deal=1)

    context = {
        'products' : products,
    }

    return render(request, 'home/index.html', context)
