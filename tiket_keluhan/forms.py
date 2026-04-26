from django import forms

class AuthForm(forms.Form):
    login_id = forms.CharField(label="Login Id", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)