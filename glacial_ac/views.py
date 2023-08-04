from django.shortcuts import render
from products.models import SubCategory


def get_subcat():
    nav_subcat = SubCategory.objects.all()
    return nav_subcat


def handler404(request, exception):
    """ Error Handler 404 - Page Not Found """
    return render(request, "errors/404.html", status=404)


def handler500(request):
    """ Error Handler 500 - Internal Server Error """
    return render(request, "errors/500.html", status=500)
