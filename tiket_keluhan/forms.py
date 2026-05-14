from django import forms
from tiket_keluhan.models import CustomUserModel, TiketModel

class AuthForm(forms.Form):
    login_id = forms.CharField(label="Login Id", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    # class Meta:
    #     model = CustomUserModel
    #     fields= ['login_id','password']
    #     widgets={
    #         'password': forms.PasswordInput
    #     }
    
class TiketForm(forms.ModelForm):
    class Meta:
        model = TiketModel
        fields = ['login_id','subject', 'description']
        widgets = {
            "login_id": forms.TextInput(attrs={"class": "form-control"}),
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }
        
        
