from django.db.models import Sum
from django.shortcuts import render, redirect
from .models import Donation, Institution, Category
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponse
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required

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

@login_required
def add_donation(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'add_donation.html', context)


def login_view(request):
    if request.method == 'POST':
        # Get the username and password from the POST request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's built-in authentication function to verify the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If the credentials are correct, log the user in
            login(request, user)
            # Redirect to the desired page after login
            return redirect(reverse('landing-page'))  # Replace 'landing-page' with your landing page view name
        else:
            # If credentials are incorrect, stay on the login page and show an error
            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })
    else:
        # If it's a GET request, just render the login page
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('landing-page')

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


@login_required
def form(request):

    categories = Category.objects.all()
    if request.method == 'POST':
        pass
    return render(request, 'form.html', {'categories': categories})