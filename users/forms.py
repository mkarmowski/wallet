from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise FormValidationError('Passwords do not match')
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, min_length=4)
    password = forms.CharField(widget=forms.PasswordInput)
