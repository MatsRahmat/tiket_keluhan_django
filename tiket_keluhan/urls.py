from django.urls import path

from tiket_keluhan import views
# from tiket_keluhan.view.auth_view import AuthView
from tiket_keluhan.views import (
    AuthView,
    DashboardView,
    TiketSubmitStatus,
    # =========== TIKET ===========
    TiketListView,
    TiketCreateView,
    TiketUpdateView,
    TiketDetailView,    
    TiketDeleteView,
    TiketAssignView,
    
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
    
    # ================================ REDIREC ================================
    path('action-message', TiketSubmitStatus.as_view(), name='message'),
    
    # ================================ TIKET ================================
    path('tiket', TiketListView.as_view(), name="list-tiket"),
    path('new-tiket', TiketCreateView.as_view(), name="create-tiket"), # un-auth page
    path('tiket/<int:pk>/detail', TiketDetailView.as_view(), name="detail-tiket"),
    # path('tiket/<int:pk>/edit', TiketDetailView.as_view(), name="edit-tiket"),
    path('tiket/<int:pk>/update', TiketUpdateView.as_view(), name="update-tiket"),
    path('tiket/<int:pk>/delete', TiketDeleteView.as_view(), name="delete-tiket"),
    path('tiket/<int:pk>/assign', TiketAssignView.as_view(), name="assign-tiket"),  
    # ================================ TIKET ================================
    path('user', UserListView.as_view(), name="user-list"),
    path('user/add', UserCreateView.as_view(), name="user-create"),
    path('user/<int:pk>/edit', UserUpdateView.as_view(), name="user-edit"),
    path('user/<int:pk>/delete', UserDeleteView.as_view(), name="user-delete"),
]
