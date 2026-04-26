from django.urls import path

from tiket_keluhan import views
from tiket_keluhan.view.auth_view import AuthView

urlpatterns = [
    path("", views.index, name="home page"),
    path("login", AuthView.as_view(), name="auth-view"),

]
