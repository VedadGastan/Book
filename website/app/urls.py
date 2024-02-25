from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('about', about, name='about'),
    path('book/<code>', book, name='book'),
    path('success/<code>', success, name='success'),
    path('cancel/<code>', cancel, name='cancel'),
    path('create-checkout-session/<code>/', checkout, name='create-checkout-session')

    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
