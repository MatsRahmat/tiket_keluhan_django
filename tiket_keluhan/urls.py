from django.urls import path

from tiket_keluhan import views
# from tiket_keluhan.view.auth_view import AuthView
from tiket_keluhan.views import (
    AuthView,
    DashboardView,
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
    UserDeleteView,
    
)

urlpatterns = [
    # path("", views.index, name="home"),
    path("", DashboardView.as_view(), name="home"),
    path("login", AuthView.as_view(), name="login"),
    path("logout", views.logout_view, name="logout"),
    
    # ================================ TIKET ================================
    path('tiket', TiketListView.as_view(), name="list-tiket"),
    path('tiket/create', TiketCreateView.as_view(), name="create-tiket"),
    path('tiket/<int:pk>/edit', TiketDetailView.as_view(), name="edit-tiket"),
    path('tiket/<int:pk>/update', TiketUpdateView.as_view(), name="update-tiket"),
    path('tiket/<int:pk>/delete', TiketDeleteView.as_view(), name="delete-tiket"),
    
    # ================================ TIKET ================================
    path('user', UserListView.as_view(), name="user-list"),
    path('user/add', UserCreateView.as_view(), name="user-create"),
    path('user/<int:pk>/edit', UserUpdateView.as_view(), name="user-edit"),
    path('user/<int:pk>/delete', UserDeleteView.as_view(), name="user-delete"),
]
