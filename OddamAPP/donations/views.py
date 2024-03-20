from django.db.models import Sum
from django.shortcuts import render, redirect
from .models import Donation, Institution
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import HttpResponse
from .forms import RegistrationForm


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

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('landing-page')
        else:
            # Dodaj informacje o błędach walidacji
            return render(request, 'register.html', {
                'form': form,
                'errors': form.errors
            })
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})
def form(request):
    return render(request, 'form.html')