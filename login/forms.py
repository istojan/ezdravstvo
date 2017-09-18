from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # the widget will hide the password from the user

    class Meta:
        model = User
        # fields = ['username', 'email', 'password']
        fields = ['username', 'password']
        help_texts = {
            'username': None,
            'email': None,
        }