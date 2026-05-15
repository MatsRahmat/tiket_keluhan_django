from django.urls import path

from tiket_keluhan import views
# from tiket_keluhan.view.auth_view import AuthView
from tiket_keluhan.views import (
    AuthView,
    # =========== TIKET ===========
    TiketListView,
    TiketCreateView,
    TiketUpdateView,
    TiketDetailView,    
    TiketDeleteView,
    
    # =========== USER ===========
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView
    
)

urlpatterns = [
    path("", views.index, name="home"),
    path("login", AuthView.as_view(), name="auth-view"),
    path("logout", views.logout_view, name="logout-view"),
    
    # ================================ TIKET ================================
    path('tiket', TiketCreateView.as_view(), name="list-tiket"),
    path('tiket/<int:pk>/edit', TiketDetailView.as_view(), name="edit-tiket"),
    path('tiket/<int:pk>/update', TiketUpdateView.as_view(), name="update-tiket"),
    path('tiket/<int:pk>/delete', TiketDeleteView.as_view(), name="delete-tiket"),
    
    # ================================ TIKET ================================
    path('user', UserListView.as_view(), name="user-list"),
    path('user/add', UserCreateView.as_view(), name="user-create"),
    path('user/<int:pk>/edit', UserUpdateView.as_view(), name="user-edit"),
    path('user/<int:pk>/delete', UserDeleteView.as_view(), name="user-delete"),
]
