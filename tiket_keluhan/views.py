from django.http import HttpResponse, request, response
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="/login")
def index(req: request):
    session = req.session.get("login_id")
    print(session)
    return render(req, "home/index.html", {})

def logout_view(req):
    logout(req)
    return redirect("/login")