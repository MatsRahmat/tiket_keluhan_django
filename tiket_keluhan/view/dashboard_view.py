from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

# class DashboardView(LoginRequiredMixin,View):
#     login_url = "login"
#     def get(req):
#         render("")