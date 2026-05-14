from django.urls import path

from tiket_keluhan import views
# from tiket_keluhan.view.auth_view import AuthView
from tiket_keluhan.views import (
    AuthView,
    # TiketView,
    # TIKET
    TiketListView,
    TiketCreateView,
    TiketUpdateView,
    TiketDetailView,    
    TiketDeleteView,
    
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
]
