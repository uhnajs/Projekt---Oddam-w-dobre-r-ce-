from django.db.models import Sum
from django.shortcuts import render, redirect
from .models import Donation, Institution
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.http import HttpResponse


def landing_page(request):
    total_bags = Donation.objects.aggregate(Sum('quantity'))
    total_institutions = Institution.objects.filter(donation__isnull=False).distinct().count()
    foundations = Institution.objects.filter(type=Institution.FOUNDATION)
    ngos = Institution.objects.filter(type=Institution.NGO)
    local_collections = Institution.objects.filter(type=Institution.LOCAL_COLLECTION)

    context = {
        'total_bags': total_bags['quantity__sum'] if total_bags['quantity__sum'] else 0,
        'total_institutions': total_institutions,
        'foundations': foundations,
        'ngos': ngos,
        'local_collections': local_collections,
    }

    return render(request, 'index.html', context)


def add_donation(request):
    return render(request, 'add_donation.html')

# Widok logowania
def login_view(request):
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['email']
        first_name = request.POST['name']
        last_name = request.POST['surname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Ten adres email jest już zajęty.')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                user.save()
                login(request, user)
                return redirect('landing-page')
        else:
            messages.error(request, 'Hasła nie są identyczne.')
            return redirect('register')
    else:
        return render(request, 'register.html')

def form(request):
    return render(request, 'form.html')