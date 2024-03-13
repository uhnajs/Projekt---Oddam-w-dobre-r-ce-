from django.shortcuts import render

def landing_page(request):
    return render(request, 'index.html')


def add_donation(request):
    return render(request, 'add_donation.html')

# Widok logowania
def login_view(request):
    return render(request, 'login.html')

# Widok rejestracji
def register(request):
    return render(request, 'register.html')