from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from tiket_keluhan.forms import AuthForm
from django.contrib.auth import authenticate, login, logout

class AuthView(View):
    def get(self, req, *args, **kwargs):
        # print("Login page")
        login_session = req.session.get("login_id")
        if login_session is not None:
            return redirect("/")
        form = AuthForm()
        return render(req, 'auth/login.html',{"form":form})

    def post(self, req, *args, **kwargs):
        form = AuthForm(req.POST)
        
        if form.is_valid():
            login_id = form.cleaned_data['login_id']
            password = form.cleaned_data['password']
            
            user = authenticate(req,login_id=login_id, password=password)
            if user:
                login(req, user)
                req.session['username'] = user.username
                req.session['user_id'] = user.id
                req.session['login_id'] = user.login_id
            else:
                print(user)
                form.add_error(None,"Login id atau password salah")
        return redirect("/")