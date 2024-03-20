from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label="Nazwa użytkownika",
        widget=forms.TextInput(attrs={'placeholder': 'Nazwa użytkownika'}),
        help_text="Wymagane. 150 znaków lub mniej. Tylko litery, cyfry oraz @/./+/-/_ ."
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
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
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if not re.search(r"\d", password):
            raise ValidationError("Hasło musi zawierać przynajmniej jedną cyfrę.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("Hasło musi zawierać przynajmniej jeden znak specjalny.")
        if len(password) < 8:
            raise ValidationError("Hasło musi zawierać przynajmniej 8 znaków.")
        return password
