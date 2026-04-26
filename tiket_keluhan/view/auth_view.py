from django.views import View
from django.http.status
from django.http import HttpResponse
from django.shortcuts import render
from tiket_keluhan.forms import AuthForm

class AuthView(View):
    
    def get(self, req, *args, **kwargs):
        form = AuthForm()
        return render(req, 'auth/login.html',{"form":form})
        

    def post(self, req, *args, **kwargs):
        data = AuthForm(req.POST)
        print(data)
        return HttpResponse("Oke",status)