from django.db.models import Sum
from django.shortcuts import render
from .models import Donation, Institution

def landing_page(request):

    total_bags = Donation.objects.aggregate(Sum('quantity'))

    total_institutions = Institution.objects.filter(donation__isnull=False).distinct().count()

    context = {
        'total_bags': total_bags['quantity__sum'],
        'total_institutions': total_institutions,
    }
    return render(request, 'index.html', context)


def add_donation(request):
    return render(request, 'add_donation.html')

# Widok logowania
def login_view(request):
    return render(request, 'login.html')

# Widok rejestracji
def register(request):
    return render(request, 'register.html')