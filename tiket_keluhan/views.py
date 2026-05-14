import json
from typing import Any
from django.views import View
from django.views.generic import (
    DetailView, UpdateView,ListView, CreateView, DeleteView
)
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, request, response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from tiket_keluhan.forms import (
    AuthForm, 
    TiketForm,
)

from tiket_keluhan.utils import (
    show_toast,
    show_toast_2,
)

from tiket_keluhan.enums import (
    MesgTitleEnum
)

from tiket_keluhan.models import (
    TiketModel
)

# ============================================
#           Global response key
# ============================================

__title = {mesg.name: mesg.value for mesg in MesgTitleEnum}

class MesgTitle:
    SUCCESS = "Berhasil"
    FAILED  = "Gagal"
    WARNING = "Peringatan"

# Create your views here.

@login_required(login_url="/login")
def index(req: request):
    session = req.session.get("login_id")
    list_tiket = TiketModel.objects.all()
    return render(req, "home/index.html", {"tickets": list_tiket})

def logout_view(req: request):
    del req.session['username']
    del req.session['user_id']
    del req.session['login_id']
    logout(req)
    return redirect("/login")

def tiket_update_delete(req, id):
    action = req.GET.get("action")
    if action == "edit":
        tiket = get_object_or_404(TiketModel,id=id)
        form = TiketForm(req.POST,instance=tiket)
        # print(form)
        if form.is_valid():
            tiket = form.save(commit=False)
            tiket.save()
        return render(req, 'tiket/form_tiket.html', {"form":form})
    elif action == "delete":
        pass

###################################################
#                   AUTH CLASS VIEW
###################################################
class AuthView(View):
    def get(self, req, *args, **kwargs):
        login_session = req.session.get("login_id")
        if login_session is not None:
            return redirect("/")
        form = AuthForm()
        return render(req, 'auth/login.html',{"form":form})

    def post(self, req, *args, **kwargs):
        form = AuthForm(req.POST)
        context = {}
        if form.is_valid():
            login_id = form.cleaned_data['login_id']
            password = form.cleaned_data['password']
            user = authenticate(req,login_id=login_id, password=password)
            if user:
                login(req, user)
                req.session['username'] = user.username
                req.session['user_id'] = user.id
                req.session['login_id'] = user.login_id
                messages.success(req,"Berhasil login")
                # context = show_toast(context, "Berhasil", "Berhasil login")
                return redirect("/", context)
            else:
                messages.error(req,"Password atau login id salah")
                context = show_toast(context, "Gagal", "Password atau login id salah")
                # print(context)
                return redirect("/login", context)
        else:
            messages.error(req,"Login id atau password tidak valid")
            context = show_toast(context, "Gagal", "Login id atau password tidak boleh kosong")
            return redirect("/login", context)
            
                


###################################################
#                   TIKET CLASS VIEW
###################################################

class TiketListView(ListView):
    model = TiketModel
    template_name = "/"

class TiketDetailView(DetailView):
    model = TiketModel
    form_class = TiketForm
    template_name="tiket/form_tiket.html"
    
    # Untuk menampilkan form dan mengisinya dengan data yg didapat
    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(instance=self.object) 
        context["action"] = "update"
        return context
    
    
class TiketCreateView(CreateView):
    model = TiketModel
    form_class = TiketForm
    template_name ="tiket/form_tiket.html"
    success_url = reverse_lazy("home")
    
    def form_valid(self, form):
        messages.success(self.request, "Tiket berhasil dibuat")
        response = super().form_valid(form)
        
        # self.extra_context = show_toast_2(MesgTitle.SUCCESS, "Tiket berhasil dibuat")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # if not context:
        #     context = {}
        # context["action"] = "add"
        
        # if hasattr(self, "extra_context") and self.extra_context:
        #     context.update(self.extra_context)
        return context
    
class TiketUpdateView(UpdateView):
    model = TiketModel
    fields = ['login_id','subject', 'description']
    template="tiket/form_tiket.html"
    # success_url = redirect(to="", permanent=True)
    success_url = reverse_lazy("home")
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # if not context:
        #     context = {}
        
        # context["action"] = "update"
    
        # if hasattr(self, "extra_context") and self.extra_context:
        #     print(self.extra_context)
        #     context.update(self.extra_context)
        # print(context)
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Tiket berhasil di ubah")
        # self.extra_context = show_toast_2(MesgTitle.SUCCESS, "Tiket berhasil di ubah")
        return response
    
    
class TiketDeleteView(DeleteView):
    model = TiketModel
    template_name = "confirm/delete.html"
    success_url = reverse_lazy("home")
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["is_delete"] = True 
        context["delete_url"] = f"/tiket/{self.object.id}/delete"
        context["back_url"] = "/"
        context["title"] = "Hapus Tiket"
        context["mesg"] = f"Apakah anda yakin ingin menghapus tiket #{self.object.no_tiket}?"
        
        context = show_toast(context, "Success")
        
        return context
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Berhasil menghapus data")
        return super().delete(request, *args, **kwargs)

    
class TiketView(View):
    def get(self, req, *args, **kwargs):
        action = req.GET.get("action")
        form = TiketForm()
        return render(req, 'tiket/form_tiket.html', {"form":form})
    
    def post(self, req, *args, **kwargs):
        if False:
            pass
        else:
            form_val = TiketForm(req.POST)
            if form_val.is_valid():
                tiket = form_val.save(commit=False)
                tiket.save()
                messages.success(req,"Tiket berhasil dibuat")
                return redirect("/tiket")
                
    def put(self, req, *args, **kwargs):
        pass
    
    def delete(self, req, *args, **kwargs):
        pass