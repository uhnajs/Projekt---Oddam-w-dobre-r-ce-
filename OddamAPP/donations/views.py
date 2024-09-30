from django.contrib import messages
from django.contrib.auth.models import User

from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Donation, Institution, Category
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import UserEditForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.views import View



@login_required
def user_settings(request):
    user = request.user

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user, request.POST)

        if user_form.is_valid():
            user_form.save()
            return redirect('user_profile')

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Zaktualizuj sesję, aby uniknąć wylogowania
            return redirect('user_profile')
    else:
        user_form = UserEditForm(instance=user)
        password_form = PasswordChangeForm(user)

    context = {
        'user_form': user_form,
        'password_form': password_form
    }

    return render(request, 'user_settings.html', context)



FOUNDATION = '1'
NGO = '2'
LOCAL_COLLECTION = '3'

def landing_page(request):
    total_bags = Donation.objects.aggregate(Sum('quantity'))
    total_institutions = Institution.objects.filter(categories__in=Donation.objects.values('categories')).distinct().count()
    foundations = Institution.objects.filter(type=FOUNDATION)
    ngos = Institution.objects.filter(type=NGO)
    local_collections = Institution.objects.filter(type=LOCAL_COLLECTION)

    context = {
        'total_bags': total_bags['quantity__sum'] if total_bags['quantity__sum'] else 0,
        'total_institutions': total_institutions,
        'foundations': foundations,
        'ngos': ngos,
        'local_collections': local_collections,
    }

    return render(request, 'index.html', context)

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
def user_profile(request):
    user = request.user
    user_donations = Donation.objects.filter(user=user)
    context = {
        'user': user,
        'donations': user_donations
    }
    return render(request, 'user_profile.html', context)


class AddDonation(View):
    """ Adds a donation record made by a user into a database. """
    def get(self, request):
        if request.user.is_authenticated:
            ctx = {'categories': Category.objects.all(),
                   'institutions': Institution.objects.all()}
            return render(request, 'form.html', ctx)
        else:
            messages.add_message(request, messages.INFO, "To make a donation you have to log in first.")
            return redirect('login')

    def post(self, request):
        number_of_bags = request.POST.get("bags")
        organization = request.POST.get("organization")
        address = request.POST.get('address')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        date = request.POST.get('data')
        time = request.POST.get('time')
        more_info = request.POST.get('more_info')
        cats_list = request.POST.getlist('categories')

        if number_of_bags != "" and organization and address != "" and city != "" \
                and postcode != "" and phone != "" and date != "" and time != "" and cats_list:

            full_address = address + ", " + city
            donation = Donation.objects.create(quantity=number_of_bags,
                                               institution=Institution.objects.get(id=organization),
                                               address=full_address,
                                               phone_number=phone,
                                               zip_code=postcode,
                                               pick_up_date=date,
                                               pick_up_time=time,
                                               pick_up_comment=more_info,
                                               user=User.objects.get(id=request.user.id))
            for i in cats_list:
                cat = Category.objects.get(id=i)
                donation.categories.add(cat)

            return render(request, 'form-confirmation.html')
        else:
            messages.add_message(request, messages.ERROR, "To make a donation you have to fill in every field.")

            return redirect('/form/')



