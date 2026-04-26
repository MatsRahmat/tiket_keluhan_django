from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from tiket_keluhan.forms import AuthForm
from django.contrib.auth import authenticate, login, logout

class AuthView(View):
    
    def get(self, req, *args, **kwargs):
        print("Login page")
        form = AuthForm()
        return render(req, 'auth/login.html',{"form":form})
        

    def post(self, req, *args, **kwargs):
        form = AuthForm(req.POST)
        # print(data)
        if form.is_valid():
            login_id = form.cleaned_data['login_id']
            password = form.cleaned_data['password']
            
            user = authenticate(req,login_id=login_id, password=password)
            if user:
                pass
            else:
                print(user)
                form.add_error(None,"Login id atau password salah")
        return HttpResponse("Oke",status=200)