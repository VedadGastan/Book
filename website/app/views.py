from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import *
from django.views.decorators.csrf import csrf_exempt


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

def book(request):
    return render(request, "book.html", {})

def success(request):
    return render(request, "success.html", {})