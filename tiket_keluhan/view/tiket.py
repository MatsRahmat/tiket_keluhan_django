from django.views import View
from django.shortcuts import render, redirect
from tiket_keluhan.forms import TiketForm

class TiketView(View):
    def get(self, req, *args, **kwargs):
        form = TiketForm()
        return render(req, 'tiket/form_tiket.html', {"form": form})
    
    def post(self, req, *args, **kwargs):
        pass
    
    def put(self, req, *args, **kwargs):
        pass
    
    def delete(self, req, *args, **kwargs):
        pass