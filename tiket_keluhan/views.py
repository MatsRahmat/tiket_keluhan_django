import json, os, uuid
from datetime import date, timedelta
from typing import Any
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import (
    DetailView, UpdateView,ListView, CreateView, DeleteView
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
    str_into_date,
    str_into_datetime
)

from tiket_keluhan.enums import (
    MesgTitleEnum,
    RoleEnum
)

from tiket_keluhan.models import (
    TiketModel,
    CustomUserModel,
    TiketAttachmentModel,
    TiketStatusHistory,
)

from tiket_keluhan.services import (
    getTiketAsDirektur
    ,getTiketAsNasabah
    ,getTiketAsOperator
    ,getTiketAsPikahKetiga
)

# ============================================
#           Global response key
# ============================================

__title = {mesg.name: mesg.value for mesg in MesgTitleEnum}

MAX_FILE_SIZE = 5 * 1024 * 1024

HTML_DATE_FORMAT = "%Y-%m-%d"

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

@login_required(login_url="/login")
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
        login_session = req.session.get("is_login")
        if login_session is not None:
            messages.success(req, "Sudah berhasil login")
            return redirect("/")
        form = AuthForm()
        return render(req, 'auth/login.html',{ form: form })
    
    def post(self, req, *args, **kwargs):
        # form = AuthForm(req.POST)
        login_id = req.POST.get("login_id", None)
        password = req.POST.get("password", None)
        
        if login_id and password:
            context = {}
            user = authenticate(req,login_id=login_id, password=password)
            if user:
                print("Auth user")
                print(user)
                login(req, user)
                req.session['username'] = user.username
                req.session['user_id']  = user.id
                req.session['login_id'] = user.login_id
                req.session['role']     = user.role
                req.session["is_login"] = True
                
                messages.success(req,"Berhasil login")
                return redirect("/", context)
            else:
                messages.error(req,"Password atau login id salah")
                return redirect("/login", context)
        
        messages.error(req,"Password atau login_id diperlukan")
        return redirect("/login", context)
        # login_as    = req.POST.get('login_as')
        # login_id    = req.POST.get('login_id')
        # # user_id     = req.POST.get('user_id')
        # password    = req.POST.get('password')
        
        # # ===== Validasi value ======
        # if not login_id:
        #     messages.error(req, "Login ID diperlukan")
        #     return redirect('/login')
        
        # # Login sebagai nasabah
        # if login_as == '1' and not user_id:
        #     messages.error(req, "User Id diperlukan")
        #     return redirect('/login')
        
        # # Login sebagai operator
        # elif login_as == '2' and not password:
        #     messages.error(req, "Password diperlukan")
        #     return redirect('/login')
        

###################################################
#                   DASHBOARD CLASS VIEW
###################################################
        
class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = "home/index.html"
    login_url = "/login"
    
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context[""] = None
        # TODO: Memuat data summary dan statistik dari tiket yg ada 
        return context
    
    
class TiketSubmitStatus(TemplateView):
    template_name = 'ui/message.html'
    
                
###################################################
#                   TIKET CLASS VIEW
###################################################

class TiketListView(LoginRequiredMixin,ListView):
    # model = TiketModel
    context_object_name = "tickets"
    template_name = "tiket/index.html"
    
    def get_queryset(self):
        role = self.request.session.get("role")
        
        # ============== Param ==============
        login_id = self.request.GET.get("login_id", "")
        tiket_no = self.request.GET.get("tiket_no", "")
        status = self.request.GET.get("status", "")
        
        # * Parse kedalam format date
        start_date = str_into_datetime(self.request.GET.get("start_date", None), HTML_DATE_FORMAT)
        end_date = str_into_datetime(self.request.GET.get("end_date", None), dt_format=HTML_DATE_FORMAT, is_end=True)
        
        # print(f"Start date {start_date} end date {end_date}")
        # print(f"Raw start_date {self.request.GET.get("start_date", None)} raw end_date {self.request.GET.get("end_date", None)}")
        tikets = []        
        if role == RoleEnum.nasabah.value:
            # Ketika user = nasabah
            print("Masuk nasabah")
            tikets = getTiketAsNasabah(login_id)
            pass
        elif role in (RoleEnum.operator.value, RoleEnum.diretur.value) :
            # ketika operation user login
            tikets = getTiketAsOperator(status=status, tiket_no=tiket_no, start_date=start_date, end_date=end_date)
            # print(tikets)
            # print("Masuk operator & direktur")
            pass
        elif role == RoleEnum.staff.value:
            # ketika staff internal
            # print("Masuk staff")
            pass
        elif role == RoleEnum.pihak_ketiga.value:
            # ketika pihak ke-3 
            # print("Masuk pihak ke3")
            pass
        else:
            # print("Role tidak valid")
            pass
        
        print(tikets)
        return tikets
    
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # login_id = self.request.session.get("login_id")
        # role = self.request.session.get("role")
        
        # # ============== Param ==============
        # login_id = self.request.GET.get("login_id", "")
        # tiket_no = self.request.GET.get("tiket_no", "")
        # status = self.request.GET.get("status", "")
        # start_date = str_into_date(self.request.GET.get("start_date", None), HTML_DATE_FORMAT)
        # end_date = str_into_date(self.request.GET.get("end_date", None), HTML_DATE_FORMAT)
        
        context["filter"] = {
            "start_date": self.request.GET.get("start_date", ""),
            "end_date": self.request.GET.get("end_date", ""),
            "tiket_no": self.request.GET.get("tiket_no", ""),
            "status": self.request.GET.get("status", "")
        }
        
        # # * Parse kedalam format date
        
        # print(f"Start date {start_date} end date {end_date}")
        # print(f"Raw start_date {self.request.GET.get("start_date", None)} raw end_date {self.request.GET.get("end_date", None)}")
        
        # print(f"Role: {type(role)} enum: f{type(RoleEnum.diretur.value)}")
        # if role == RoleEnum.nasabah.value:
        #     # Ketika user = nasabah
        #     print("Masuk nasabah")
        #     context["tickets"] = getTiketAsNasabah(login_id)
        #     pass
        # elif role in (RoleEnum.operator.value, RoleEnum.diretur.value) :
        #     # ketika operation user login
        #     tikets = getTiketAsOperator(status=status, tiket_no=tiket_no, start_date=start_date, end_date=end_date)
        #     print(tikets)
        #     context["tickets"] = tikets
        #     print("Masuk operator & direktur")
        #     pass
        # elif role == RoleEnum.staff.value:
        #     print("Masuk staff")
        #     # ketika staff internal
        #     pass
        # elif role == RoleEnum.pihak_ketiga.value:
        #     print("Masuk pihak ke3")
        #     # ketika pihak ke-3 
        #     pass
        # else:
        #     print("Role tidak valid")
        #     context["tickets"] = []
            
        #     pass
            
        # all_tikets = TiketModel.objects.count()
        # print("Tiket count is %d " % all_tikets)
        
        

        
        # print(context)
        return context
    

class TiketDetailView(LoginRequiredMixin,DetailView):
    model           = TiketModel
    # form_class      = TiketForm
    template_name   = "tiket/detail.html"
    login_url       = "login"  # Fallback url ketika belum login
    context_object_name = 'tiket'
    
    # Untuk menampilkan form dan mengisinya dengan data yg didapat
    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        # context["form"] = self.form_class(instance=self.object) 
        # context["action"] = "update"
        # print(self.object)
        attachment = getattr(self.object, "attachment", None)
        if attachment:
            context["attachment"] = attachment
        return context
    
class TiketCreateView(CreateView):
    model           = TiketModel
    form_class      = TiketForm
    template_name   ="tiket/form_tiket.html"
    success_url     = reverse_lazy("message")
    
    def form_valid(self, form):
        response = super().form_valid(form)
        file = self.request.FILES.get('file')
        if file:
            # validasi file size
            if file.size > MAX_FILE_SIZE:
                form.add_error('file', 'Maximum file size adalah 5MB')
                return self.form_invalid(form)
            
            ext = os.path.splitext(file.name)[1].lower()
            allowed_ext = ['.png','.jpg','.jpeg']
            if ext not in allowed_ext:
                form.add_error('file', 'Extensi file tidak sesuai, hanya untuk PNG,JPG,JPEG')
                return self.form_invalid(form)
            
            today = date.today().strftime("%Y%m%d")
            new_name = f"{today}-{uuid.uuid4().hex}{ext}"
            
            TiketAttachmentModel.objects.create(
                tiket=self.object,
                file=file,
                # original_name=file.name,
                sotred_name=new_name
                )
        messages.success(self.request, "Tiket Berhasil dibuat")
        return response
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context
    
class TiketUpdateView(LoginRequiredMixin,UpdateView):
    # model       = TiketModel
    # fields      = ['login_id','subject', 'description']
    # template    ="tiket/form_tiket.html"
    # success_url = reverse_lazy("tiket-list")
    login_url   = "login" # Fallback url ketika belum login
    http_method_names = ['post']
    
    # def get_context_data(self, **kwargs) -> dict[str, Any]:
    #     context = super().get_context_data(**kwargs)
    #     context["action"] = "update"
    #     return context
    
    def post(self, req, *args, **kwargs):
        """Method post untuk update tiket langsung menjadi Done atau Riject"""
        tiket_id = self.kwargs.get("pk")
        new_status = self.request.POST.get("status")
        try:
            tiket = TiketModel.objects.get(id=tiket_id)
            tiket.status = new_status
            tiket.save()
            messages.success(req, "Berhasil ubah status tiket %s menjadi %s" % (tiket, new_status))
        except TiketModel.DoesNotExist as de:
            print("data not found %s" % de)
            messages.error(req, "Tiket tidak ditemukan, gagal update status tiket")

        return redirect("/tiket")
    
    
    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     messages.success(self.request, "Tiket berhasil di ubah")
    #     file = self.request.FILES.get("file")
    #     attachment = getattr(self.object, "attachment")
    #     if file:
    #         print("File baru ditemukan")
    #         # validasi file size
    #         if file.size > MAX_FILE_SIZE:
    #             form.add_error('file', 'Maximum file size adalah 5MB')
    #             return self.form_invalid(form)
            
    #         ext = os.path.splitext(file.name)[1].lower()
    #         allowed_ext = ['.png','.jpg','.jpeg']
    #         if ext not in allowed_ext:
    #             form.add_error('file', 'Extensi file tidak sesuai, hanya untuk PNG,JPG,JPEG')
    #             return self.form_invalid(form)
            
    #         today = date.today().strftime("%Y%m%d")
    #         new_name = f"{today}-{uuid.uuid4().hex}{ext}"
            
    #         if attachment:
    #             attachment.file = file
    #             attachment.original_name = file.name
    #             attachment.stored_name = new_name
    #             attachment.save()
    #         else:
    #             TiketAttachmentModel.objects.create(
    #                 tiket=self.object,
    #                 file=file,
    #                 sotred_name=new_name, # original name handle by model save method
    #             )
    #     else:
    #         pass
    #         print("File tidak berubah")
            
    #     return response
    
class TiketDeleteView(LoginRequiredMixin,DeleteView):
    model           = TiketModel
    template_name   = "confirm/delete.html"
    success_url     = reverse_lazy("list-tiket")
    login_url       = "login" # Fallback url ketika belum login
    http_method_names = ['post']
    
    def delete(self, request, *args, **kwargs):
        print("Success delete tiket")
        messages.success(request, "Berhasil menghapus data")
        return super().delete(request, *args, **kwargs)

    
###################################################
#                   USER CLASS VIEW
###################################################
class UserListView(LoginRequiredMixin,ListView):
    model               = CustomUserModel
    template_name       = "user/list_user.html"
    context_object_name = "list_user"
    login_url           = "login" # Fallback url ketika belum login
    
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
    model               = CustomUserModel
    template_name       = "user/user_form.html"
    form_class          = UserForm
    http_method_names   = ["get", "post"]
    success_url         = reverse_lazy("user-list")
    login_url           = "login" # Fallback url ketika belum login
    
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
    model               = CustomUserModel
    template_name       = "user/user_form.html"
    form_class          = UserForm
    http_method_names   = ["get", "post"]
    success_url         = reverse_lazy("user-list")
    login_url           = "login" # Fallback url ketika belum login
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(instance=self.object)
        context["action"] = "update" 
        return context

class UserDeleteView(LoginRequiredMixin,DeleteView):
    model         = CustomUserModel
    template_name = "user/list_user.html"
    success_url   = reverse_lazy("user-list")
    login_url     = "login" # Fallback url ketika belum login
    
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
        