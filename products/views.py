from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, SubCategory, Category
from .forms import ProductForm, SubCategoryForm, CategoryForm

def all_products(request):
    """ A view to show all products """

    products = Product.objects.all()
    query = None
    subcategories= None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'subcategory':
                sortkey = 'subcategory__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        # Handels Subcategory selection and returns subcategory and all products in it
        if 'subcategory' in request.GET:
            subcategories = request.GET['subcategory'].split(',')
            products = products.filter(subcategory__name__in=subcategories)
            subcategories = SubCategory.objects.filter(name__in=subcategories)

        # Handels search query in searchbar and returns products fitting that search
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)
    
    current_sorting = f'{sort}_{direction}'

    context = {
        'products' : products,
        'search_term' : query,
        'current_categories' : subcategories,
        'current_sorting' : current_sorting,
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


def add_category(request):
    """ Add a product to the store"""

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_category'))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = CategoryForm()

    template = 'products/add_category.html'
    context = {
        'form' : form,
    }

    return render(request, template, context)


def add_subcategory(request):
    """ Add a product to the store"""

    if request.method == 'POST':
        form = SubCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_subcategory'))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = SubCategoryForm()

    template = 'products/add_subcategory.html'
    context = {
        'form' : form,
    }

    return render(request, template, context)

def add_product(request):
    """ Add a product to the store"""

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form' : form,
    }

    return render(request, template, context)

