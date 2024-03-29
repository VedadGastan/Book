from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('about', about, name='about'),
    path('book/<code>', book, name='book'),
    path('success/<new_code>', success, name='success'),
    path('cancel/<new_code>', cancel, name='cancel'),
    path('create-checkout-session/<new_code>', checkout, name='create-checkout-session'),
    path('checkout_crypto/<new_code>', checkout_crypto, name='checkout_crypto'),
    path('signup', sign_up, name='signup'),
    path('verify_account/<code>', verify_account, name='verify_account'),
    path('login', log_in, name='login'),
    path('logout', log_out, name='logout'),
    path('delete_mail', delete_mail, name='delete_mail'),
    path('delete/<code>', delete, name='delete'),
    path('dashboard', dashboard, name='dashboard'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
