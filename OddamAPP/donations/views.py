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
    if request.method == 'POST':
        step = request.POST.get('step', '1')
        if step == '1':
            selected_categories = request.POST.getlist('categories')
            request.session['selected_categories'] = selected_categories
            return redirect(f'{reverse("form")}?step=2')
        elif step == '2':
            number_of_bags = request.POST.get('bags')
            request.session['number_of_bags'] = number_of_bags
            return redirect(f'{reverse("form")}?step=3')
        elif step == '3':
            selected_institution = request.POST.get('institution')
            request.session['selected_institution'] = selected_institution
            return redirect(f'{reverse("form")}?step=4')
        elif step == '4':
            pickup_details = {
                'address': request.POST.get('address'),
                'city': request.POST.get('city'),
                'zip_code': request.POST.get('zip_code'),
                'phone_number': request.POST.get('phone_number'),
                'pick_up_date': request.POST.get('pick_up_date'),
                'pick_up_time': request.POST.get('pick_up_time'),
                'pick_up_comment': request.POST.get('pick_up_comment'),
            }
            request.session['pickup_details'] = pickup_details
            return redirect(f'{reverse("form")}?step=summary')
    else:
        step = request.GET.get('step', '1')
        categories = Category.objects.all() if step == '1' else None
        institutions = Institution.objects.all() if step == '3' else None
        selected_categories = request.session.get('selected_categories', [])
        number_of_bags = request.session.get('number_of_bags', '')
        selected_institution = request.session.get('selected_institution', '')
        pickup_details = request.session.get('pickup_details', {})

        context = {
            'step': step,
            'categories': categories,
            'selected_categories': selected_categories,
            'number_of_bags': number_of_bags,
            'institutions': institutions,
            'selected_institution': selected_institution,
            'pickup_details': pickup_details,
        }
        return render(request, 'form.html', context)



# @login_required
# def form_summary(request):
#     # Pobieranie danych z sesji
#     selected_categories = request.session.get('selected_categories', [])
#     number_of_bags = request.session.get('number_of_bags')
#     selected_institution = request.session.get('selected_institution')
#     pickup_details = request.session.get('pickup_details', {})
#
#     # Tutaj możesz przekształcić ID kategorii na ich nazwy, jeśli jest taka potrzeba
#     categories = Category.objects.filter(id__in=selected_categories)
#
#     # Podobnie z instytucją
#     institution = Institution.objects.get(id=selected_institution)
#
#     context = {
#         'categories': categories,
#         'number_of_bags': number_of_bags,
#         'institution': institution,
#         'pickup_details': pickup_details,
#     }
#
#     return render(request, 'form_summary.html', context)


@login_required
def add_donation(request):
    if request.method == 'POST':
        # Tutaj przetwarzasz wybrane kategorie
        selected_categories_ids = request.POST.getlist('categories')
        request.session['selected_categories'] = selected_categories_ids
        # Przekierowujesz do następnego kroku
        return redirect('select_institution')  # Załóżmy, że tak nazywa się widok wyboru instytucji

    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'add_donation.html', context)

@login_required
def select_institution(request):
    selected_categories = request.session.get('selected_categories')
    institutions = Institution.objects.filter(categories__id__in=selected_categories).distinct()
    context = {'institutions': institutions}
    return render(request, 'select_institution.html', context)