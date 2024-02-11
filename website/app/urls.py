from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('about', about, name='about'),
    path('book', book, name='book'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
