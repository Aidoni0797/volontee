from django import forms
from django.contrib.auth.models import User


class AuthUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(),
            'password': forms.PasswordInput(),
        }
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }

class RegUserForm(forms.Form):
    username = forms.CharField(max_length=100, min_length=5)
    email = forms.EmailField()
    password1 = forms.CharField(max_length=100, min_length=8, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=100, min_length=8, widget=forms.PasswordInput())


class CreatePlayer(forms.Form):
    first_name = forms.CharField(max_length=255, min_length=5)
    user = forms.CharField(max_length=500, min_length=5)

class AddCard(forms.Form):
    cards_suits = forms.CharField(max_length=15, min_length=15)
    cards_ranks = forms.CharField(max_length=15, min_length=15)

class ConnectionWithVolonteer(forms.Form):
    name = forms.CharField(max_length=255, min_length=10)
    tele = forms.CharField(max_length=255, min_length=10)
    number = forms.CharField(max_length=255, min_length=10)
    text = forms.CharField(max_length=255, min_length=10)

class GetToken(forms.Form):
    your_token = forms.CharField(max_length=255, min_length=10)
    your_chat_id = forms.CharField(max_length=255, min_length=10)

