from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .models import *
from .forms import CreateUserForm
import stripe
from django.contrib.auth.decorators import login_required
import json
import requests
from django.core.mail import send_mail, EmailMessage
from django.utils.html import strip_tags
import os

stripe.api_key = settings.STRIPE_SECRET_KEY

# Payment pain
def checkout(request, new_code):
    if request.method == "POST":
        domain = settings.DOMAIN
        if settings.DEBUG:
            user = NewUser.objects.get(secondary_code=new_code)
            checkout_session = stripe.checkout.Session.create(
                mode='payment',
                line_items=[
                    {
                        'price': 'price_1P8OtFFUBznuiHclMpN8uRhM',
                        'quantity': 1,
                    },
                ],

                success_url=domain + '/success/' + str(new_code) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url = domain + '/cancel/' + str(new_code),
            )
        return redirect(checkout_session.url, code=303)

def success(request, new_code):
    session_id = request.GET.get('session_id')
    if not session_id:
        return render(request, "error.html", {"message": "Session ID is missing."})
    
    checkout_session = stripe.checkout.Session.retrieve(session_id)
    customer_email = checkout_session.customer_details.email

    if NewUser.objects.filter(secondary_code=new_code).exists():
        user = NewUser.objects.get(secondary_code=new_code)
        price = settings.AFFILIATE_PERCENTAGE * 0.5 * 100
        user.secondary_code = None
        user.balance += price
        user.sales += 1
        user.save()

        pdf_path = os.path.join(settings.BASE_DIR, 'static', 'book', 'The Dreamer - Din Cosic.pdf')
        
        subject = 'Payment Confirmation - Din Cosic'
        html_message = f"""
        <p>Hi, thank you for your purchase! You can find your copy of the book attached below.</p>
        """
        plain_message = strip_tags(html_message)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [customer_email]
        
        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as pdf_file:
                email = EmailMessage(
                    subject,
                    plain_message,
                    email_from,
                    recipient_list,
                )
                email.attach('The Dreamer - Din Cosic.pdf', pdf_file.read(), 'static/book/')
                email.content_subtype = 'html'
                email.send()
        else:
            return render(request, "error.html", {"message": "Book PDF not found."})

    return render(request, "success.html", {})

def cancel(request, new_code):
    if NewUser.objects.filter(secondary_code=new_code).exists():
        user = NewUser.objects.get(secondary_code=new_code)
        code = user.code
        user.save()
    return render(request, "cancel.html", {'code':code})


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
        user.clicks += 1
        user.save()
    return render(request, "book.html", {'new_code':new_code, 'code':code, })

def sign_up(request):
    logout(request)
    form = CreateUserForm()
    if request.method=="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(request, username=username, password=password)
            user.country = request.POST.get('country')
            user.save()

            subject = 'Account Confirmation - Din Cosic Affiliate'
            mail_link = settings.DOMAIN + '/verify_account/' + user.code
            html_message = """<p>Hi """+ user.username +""", thank you for becoming a part of our affiliate program! To finish setting up your account, click the link below.</p>

<a href='""" + mail_link + """'>""" + mail_link + """</a>"""
            plain_message = strip_tags(html_message)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail( subject, plain_message, email_from, recipient_list, fail_silently=False )

            messages.success(request, "Check your email to verify your account.")
            return redirect('home')

    return render(request, "signup.html", {'form':form})

def verify_account(request, code):
    user = NewUser.objects.get(code=code)
    user.verified = True
    stripe_account = stripe.Account.create(
        type="express",
        country=user.country,
        email= user.email,
        capabilities={
            "card_payments": {"requested": True},
            "transfers": {"requested": True},
        },
        business_type = 'individual',
        business_profile= {
            "mcc": 5815,
            "url": "https://www.instagram.com/dincosic/",
        }
    )

    link = stripe.AccountLink.create(
        account = stripe_account.id,
        refresh_url = settings.DOMAIN + "/delete",
        return_url = settings.DOMAIN + "/dashboard",
        type = "account_onboarding",
    )
    if(stripe_account.id and link):
        user.stripe_id = stripe_account.id
        user.save()
        login(request, user)
        return redirect(link.url)
    
    user.delete()
    messages.info(request, "An error occurred while creating your account. Please try again!")
    return redirect("signup")


def log_in(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else: 
            messages.info(request, "Username or password incorrect!")

    return render(request, "login.html", {})

def log_out(request):
    logout(request)
    return redirect('login')

@login_required
def delete_mail(request):
    user = request.user
    subject = 'Account deletion - Din Cosic Affiliate'
    mail_link = settings.DOMAIN + '/delete/' + user.code
    html_message = """<p>We are sorry to se you go! To proceed with deleting your account, click the link below.</p>

<a href='""" + mail_link + """'>""" + mail_link + """</a>"""
    plain_message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    send_mail( subject, plain_message, email_from, recipient_list, fail_silently=False )

    messages.success(request, "Go to your email, to finalize deleting your account.")
    return redirect('dashboard')

@login_required
def delete(request, code):
    user = NewUser.objects.get(code=code)
    if(user.stripe_id):
        stripe_id = user.stripe_id
        stripe.Account.delete(stripe_id)
    user.delete()
    messages.success(request, "Your account has been deleted")
    return redirect('home')

@login_required
def dashboard(request):
    user = request.user

    if(user.verified):
        if(not stripe.Account.retrieve(user.stripe_id)["payouts_enabled"]):
            messages.info(request, "There has been an error while creating your account, please try again!")
            return redirect('delete', user.code)
        username = user.username
        balance = user.balance / 100
        clicks = user.clicks
        sales = user.sales
        code = settings.DOMAIN + '/book/' + user.code
        if(clicks!=0):
            conversion = int(sales/clicks*100)
        else:
            conversion = 0

        context = {
            'username' : username, 
            'balance' : balance,
            'clicks' : clicks,
            'sales' : sales,
            'code' : code,
            'conversion' : conversion,
            'user_code' :  user.code,
        }

        return render(request, "dashboard.html", context)
    
    return redirect('home')

def checkout_crypto(request, new_code):
    url = "https://api.nowpayments.io/v1/invoice"

    success_url = settings.DOMAIN + '/success/' + str(new_code)
    cancel_url = settings.DOMAIN + '/cancel/' + str(new_code)

    rand = ''.join(random.choices(string.digits, k=5))

    payload = json.dumps({
        "price_amount": 7.77,
        "price_currency": "usd",
        "order_id": "RGDBP-"+rand,
        "order_description": "The Dreamer",
        "ipn_callback_url": "https://nowpayments.io",
        "success_url": success_url,
        "cancel_url": cancel_url,
        "partially_paid_url": cancel_url,
        "is_fixed_rate": True,
        "is_fee_paid_by_user": False
    })
    headers = {
        'x-api-key': settings.NOWPAYMENTS_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    url = json.loads(response.text)["invoice_url"]
    return redirect(url)
