from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.shortcuts import get_object_or_404

stripe.api_key = settings.STRIPE_SECRET_KEY

# Payment pain
def checkout(request, code):
    if request.method == "POST":
        domain = settings.DOMAIN
        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1OmFklFUBznuiHclWqPnuqzr',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url = domain + '/success/' + code,
            cancel_url = domain + '/cancel' + code,
        )
        return redirect(checkout_session.url, code=303)

def home(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if Email.objects.filter(email=email).exists():
            messages.success(request, ("You are already subscibed to our newsletter!"))
            return redirect('home')

        Email.objects.create(email=email)
        messages.success(request, ("You have successfully subscribed to our newsletter!"))
        return redirect('home')
    return render(request, "home.html", {})

def about(request):
    return render(request, "about.html", {})

def book(request, code):
    return render(request, "book.html", {})

def cancel(request, code):
    return render(request, "cancel.html", {})

def success(request, code):
    return render(request, "success.html", {})