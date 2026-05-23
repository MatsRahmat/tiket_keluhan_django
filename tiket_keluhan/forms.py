from django import forms
from tiket_keluhan.models import CustomUserModel, TiketModel, TiketActionModel
from tiket_keluhan.enums import (
    RoleEnum
)

class AuthForm(forms.Form):
    # login_id = forms.TextInput(attrs={"class": "form-control"})
    # password = forms.PasswordInput(attrs={"class": "form-control"})
    class Meta:
        model = CustomUserModel
        fields= ['login_id','password']
        widgets={
            'login_id': forms.PasswordInput(attrs={"class": "form-control"}),
            'password': forms.TextInput(attrs={"class": "form-control"})
        }
    
class TiketForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={"class": "form-control", "required": False}))
    class Meta:
        model = TiketModel
        fields = ['login_id','subject', 'description', 'file']
        widgets = {
            "login_id": forms.TextInput(attrs={"class": "form-control"}),
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }
        

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUserModel
        fields = ['login_id','username', 'role']
        widgets = {
            'login_id': forms.TextInput(attrs={"class": "form-control"}),
            'username': forms.TextInput(attrs={"class": "form-control"}),
            # 'password': forms.PasswordInput(attrs={"class": "form-control"}),
            'role': forms.Select(attrs={"class": "form-control"}, choices=[(r.value, r.name.replace("_", " ").title()) for r in RoleEnum][1:]),
        }
    
    # def __init__(self, *args, **kwargs):
    #     roles = kwargs.pop("roles", None)
    #     super().__init__(*args, **kwargs)
    #     if roles:
    #         self.fields["role"].widget = forms.Select(
    #         choices=roles,
    #         attrs={ "class": "form-select" }
    #         )



class TiketActionForm(forms.ModelForm):
    class Meta:
        model = TiketActionModel
        fields = ['tiket', 'aktor', 'action_type','note']