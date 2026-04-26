from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(req):
    return render(req, "home/index.html", {})

def login(req):
    return render(req, 'auth/login.html', {})
    # return HttpResponse("ini halaman update lagi login nya")