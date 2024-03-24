from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs={'placeholder': 'Email'}),
        help_text="Wymagane. Wprowadź ważny adres e-mail."
    )
    first_name = forms.CharField(
        label="Imię",
        widget=forms.TextInput(attrs={'placeholder': 'Imię'})
    )
    last_name = forms.CharField(
        label="Nazwisko",
        widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'})
    )
    password1 = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}),
        help_text="Hasło musi zawierać co najmniej 8 znaków oraz zawierać cyfrę i znak specjalny."
    )
    password2 = forms.CharField(
        label="Potwierdzenie hasła",
        widget=forms.PasswordInput(attrs={'placeholder': 'Potwierdź hasło'}),
        help_text="Wprowadź to samo hasło, dla weryfikacji."
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # Use email as username
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
