import json
from typing import Any
from django.views import View
from django.views.generic import (
    DetailView, UpdateView,ListView, CreateView, DeleteView,
)
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, request, response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from tiket_keluhan.forms import (
    AuthForm, 
    TiketForm,
    UserForm
)

from tiket_keluhan.utils import (
    show_toast,
    show_toast_2,
    context_modal_delete,
)

from tiket_keluhan.enums import (
    MesgTitleEnum,
    RoleEnum
)

from tiket_keluhan.models import (
    TiketModel,
    CustomUserModel,
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
    del req.session['is_login']
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
            messages.success(req, "Sudah berhasil login")
            return redirect("/")
        return render(req, 'auth/login.html',)

    def post(self, req, *args, **kwargs):
        login_as = req.POST.get('login_as')
        login_id = req.POST.get('login_id')
        user_id = req.POST.get('user_id')
        password = req.POST.get('password')
        
        # ===== Validasi value ======
        if not login_id:
            messages.error(req, "Login ID diperlukan")
            return redirect('/login')
        
        # Login sebagai nasabah
        if login_as == '1' and not user_id:
            messages.error(req, "User Id diperlukan")
            return redirect('/login')
        
        # Login sebagai operator
        elif login_as == '2' and not password:
            messages.error(req, "Password diperlukan")
            return redirect('/login')
            
        context = {}
        user = authenticate(req,login_id=login_id, password=password)
        if user:
            login(req, user)
            req.session['username'] = user.username
            req.session['user_id'] = user.id
            req.session['login_id'] = user.login_id
            req.session["is_login"] = True
            messages.success(req,"Berhasil login")
            return redirect("/", context)
        else:
            messages.error(req,"Password atau login id salah")
            return redirect("/login", context)
        
                
###################################################
#                   TIKET CLASS VIEW
###################################################

class TiketListView(ListView):
    model = TiketModel
    template_name = "/"

class TiketDetailView(LoginRequiredMixin,DetailView):
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
    
    
class TiketUpdateView(LoginRequiredMixin,UpdateView):
    model = TiketModel
    fields = ['login_id','subject', 'description']
    template="tiket/form_tiket.html"
    # success_url = redirect(to="", permanent=True)
    success_url = reverse_lazy("home")
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # if not context:
        #     context = {}
        
        context["action"] = "update"
    
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
    
    
class TiketDeleteView(LoginRequiredMixin,DeleteView):
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
        
        # context = show_toast(context, "Success")
        
        return context
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Berhasil menghapus data")
        return super().delete(request, *args, **kwargs)

    
###################################################
#                   USER CLASS VIEW
###################################################
class UserListView(LoginRequiredMixin,ListView):
    model = CustomUserModel
    template_name = "user/list_user.html"
    context_object_name = "list_user"
    
    def get_queryset(self):
        qs = super().get_queryset()
        for user in qs:
            try:
                user.role_label = RoleEnum(user.role).name.replace("_", "").title()
            except ValueError:
                user.role_label = "Unknown"
        return qs
        # return super().get_queryset()
    
class UserCreateView(LoginRequiredMixin,CreateView):
    model = CustomUserModel
    template_name = "user/user_form.html"
    form_class = UserForm
    http_method_names = ["get", "post"]
    success_url = reverse_lazy("user-list")
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["action"] = "add"
        print("Get context")
        return context
    
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs["roles"] = [(r.value, r.name.replace("_", " ").title()) for r in RoleEnum][1:]
    #     print("set kwargs")
    #     return kwargs

class UserUpdateView(LoginRequiredMixin,UpdateView):
    model = CustomUserModel
    template_name = "user/user_form.html"
    form_class = UserForm
    http_method_names = ["get", "post"]
    success_url = reverse_lazy("user-list")
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(instance=self.object)
        context["action"] = "update" 
        return context

class UserDeleteView(LoginRequiredMixin,DeleteView):
    model = CustomUserModel
    template_name = "user/list_user.html"
    success_url = reverse_lazy("user-list")
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        context = context_modal_delete(context, "Hapus User", f"Apakah anda yakin ingin menghapus {obj.username}?", f"/user/{obj.id}/delete", "/user") 
        return context
    
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        # Validasi goes here
        if obj.id == request.user.user_id:
            messages.error(request, "TIdak dapat menghapus akun milik sendiri")
        elif obj.role == RoleEnum.diretur.value:
            messages.error(request, "Tidak dapat menghapus user dengan role direktur")
        else:
            super().delete(request, *args, **kwargs)
        
        return reverse_lazy('user-list')
        