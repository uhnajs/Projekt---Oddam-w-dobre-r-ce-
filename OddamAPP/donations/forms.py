from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'custom-class'}), label='', help_text=None)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło', 'class': 'custom-class'}), label='', help_text=None)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Potwórz hasło', 'class': 'custom-class'}), label='', help_text=None)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nazwa użytkownika', 'class': 'custom-class'}),
        }
        help_texts = {
            'username': None,
        }