from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, min_length=4)
    password = forms.CharField(widget=forms.PasswordInput)
