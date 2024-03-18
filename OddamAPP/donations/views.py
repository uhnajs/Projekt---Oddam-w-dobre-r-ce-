from django.db.models import Sum
from django.shortcuts import render, redirect
from .models import Donation, Institution
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.http import HttpResponse
from .forms import RegisterForm


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
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def form(request):
    return render(request, 'form.html')