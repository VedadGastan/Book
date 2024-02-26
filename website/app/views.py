from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .models import *
from .forms import CreateUserForm
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Payment pain
def checkout(request, new_code):
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
            success_url = domain + '/success/' + str(new_code),
            cancel_url = domain + '/cancel' + str(new_code),
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
    if NewUser.objects.filter(code=code).exists():
        user = NewUser.objects.get(code=code)
        new_code = generate_code()
        user.secondary_code = new_code
        user.save()
    return render(request, "book.html", {'new_code':new_code,})

def success(request, new_code):
    if NewUser.objects.filter(secondary_code=new_code).exists():
        user = NewUser.objects.get(secondary_code=new_code)
        new_code = None
        price = settings.AFFILIATE_PERCENTAGE * 0.5 * 100
        user.secondary_code = new_code
        user.balance += price
        user.save()
    return render(request, "success.html", {})

def cancel(request, new_code):
    return render(request, "cancel.html", {})

def sign_up(request):
    form = CreateUserForm()
    if request.method=="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('home')

    return render(request, "signup.html", {'form':form})


def log_in(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else: 
            messages.info(request, "Username or password incorrect!")

    return render(request, "login.html", {})

def log_out(request):
    logout(request)
    return redirect('login')