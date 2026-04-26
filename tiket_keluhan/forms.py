from django import forms
from tiket_keluhan.models import CustomUserModel

class AuthForm(forms.Form):
    login_id = forms.CharField(label="Login Id", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    # class Meta:
    #     model = CustomUserModel
    #     fields= ['login_id','password']
    #     widgets={
    #         'password': forms.PasswordInput
    #     }