from .views import handler404, handler500
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls')),
    path('profile/', include('profiles.urls')),
    path('summernote/', include('django_summernote.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#Error handling
handler404 = 'glacial_ac.views.handler404'
handler500 = 'glacial_ac.views.handler500'