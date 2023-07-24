from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from .models import Product, SubCategory


def all_products(request):
    """ A view to show all products """

    products = Product.objects.all()
    query = None
    subcategories= None

    if request.GET:
        if 'subcategory' in request.GET:
            subcategories = request.GET['subcategory'].split(',')
            products = products.filter(subcategory__name__in=subcategories)
            subcategories = SubCategory.objects.filter(name__in=subcategories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)
    context = {
        'products' : products,
        'search_term' : query,
        'current_categories' : subcategories,
    }
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show product details """
    product = get_object_or_404(Product, pk=product_id)
    subcategory = product.subcategory
    category = Product.objects.filter(subcategory=subcategory)
    paginator = Paginator(category, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'product' : product,
        'page_obj' : page_obj,
    }
    return render(request, 'products/product_detail.html', context)