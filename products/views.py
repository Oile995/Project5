from django.shortcuts import (
    render, redirect, reverse, get_object_or_404
)
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, SubCategory, Category, Review
from .forms import (
    ProductForm, SubCategoryForm, CategoryForm, ReviewForm
)


def all_products(request):
    """ A view to show all products """

    products = Product.objects.all()
    query = None
    subcategories = None
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

        # Handels Subcategory selection and returns
        # subcategory and all products in it
        if 'subcategory' in request.GET:
            subcategories = request.GET['subcategory'].split(',')
            products = products.filter(subcategory__name__in=subcategories)
            subcategories = SubCategory.objects.filter(name__in=subcategories)

        # Handels search query in searchbar and returns
        # products fitting that search
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria")
                return redirect(reverse('products'))
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'
    context = {
        'products': products,
        'search_term': query,
        'current_categories': subcategories,
        'current_sorting': current_sorting,
    }
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show product details """
    product = get_object_or_404(Product, pk=product_id)
    related_products = Product.objects.filter(subcategory=product.subcategory).order_by('-id')[:4]
    icons = product.icons.all()
    reviews = product.reviews.all()
    subcategory = product.subcategory
    category = Product.objects.filter(subcategory=subcategory)
    on_wishlist = False
    if product.users_wishlist.filter(id=request.user.id).exists():
        on_wishlist = True
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'reviewed': False,
        'icons': icons,
        'on_wishlist': on_wishlist,
        'review_form': ReviewForm(),
    }
    return render(request, 'products/product_detail.html', context)


# Submit review

def submit_review(request, product_id):
    """
    Submitting New and updating old Reviews depending on user.
    Updating comment and rating.
    Taken from https://github.com/dev-rathankumar/greatkart-pre-deploy\
                                                /blob/main/store/views.py
    """
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, pk=product_id)
            review = Review.objects.get(user__id=request.user.id,
                                        product__id=product_id)
            form = ReviewForm(request.POST, instance=review)
            form.save()
            messages.success(request,
                             'Thank you! Your review has been updated.')
            return HttpResponseRedirect(reverse('product_detail',
                                                args=[product.id]))

        except Review.DoesNotExist:
            product = get_object_or_404(Product, pk=product_id)
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = Review()
                data.rating = form.cleaned_data['rating']
                data.comment = form.cleaned_data['comment']
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request,
                                 'Thank you! Your review has been submitted.')
                return redirect(reverse('product_detail', args=[product_id]))


# User option to add product to wishlist
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request,
                         product.name + " has been removed from your WishList")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, "Added " + product.name + "to your WishList")
    return redirect(reverse('product_detail', args=[product_id]))


# SuperUser add view functions for Category, Subcategory and Products
@login_required
def add_category(request):
    """ Add a product to the store"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_category'))
        else:
            messages.error(request,
                           'Failed to add product.\
                           Please ensure the form is valid.')
    else:
        form = CategoryForm()

    template = 'products/add_category.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_subcategory(request):
    """ Add a product to the store"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = SubCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_subcategory'))
        else:
            messages.error(request, 'Failed to add product.\
                                    Please ensure the form is valid.')
    else:
        form = SubCategoryForm()

    template = 'products/add_subcategory.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_product(request):
    """ Add a product to the store"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product.\
                                    Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


# SuperUser Edit view functions for Products
@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product.\
                                    Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


# SuperUser Delete view functions for Products
@login_required
def delete_product(request, product_id):
    """ Delete a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
