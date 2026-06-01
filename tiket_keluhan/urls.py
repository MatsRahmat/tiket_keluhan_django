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
    
    # =========== TIKET History ===========
    TiketHistoryListView,
    
    # =========== TIKET Review ===========
    TiketReviewList,
    TiketReviewForm,
    TiketReviewDetail,
    
    # =========== TIKET Action/Assignment ===========
    TiketAssignView,
    TiketActionList,
    TiketActionView,
    
    # =========== USER ===========
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    
)

urlpatterns = [
    path("", DashboardView.as_view(), name="home"),
    path("login", AuthView.as_view(), name="login"),
    path("logout", views.logout_view, name="logout"),
    
    # ================================ REDIREC ================================
    path('action-message', TiketSubmitStatus.as_view(), name='message'),
    
    # ================================ TIKET HISTORY ================================
    path('tiket-history', TiketHistoryListView.as_view(), name="list-tiket-history"),
    
    # ================================ TIKET REVIEW ================================
    path('tiket-review', TiketReviewList.as_view(), name="list-tiket-review"),
    path('tiket-review/<int:pk>/add', TiketReviewForm.as_view(), name='add-tiket-review'),
    path('tiket-review/<int:pk>/detail', TiketReviewDetail.as_view(), name='detail-tiket-review'),
    
    # ================================ TIKET ACTION ================================
    path('tiket/actions', TiketActionList.as_view(), name="list-action-tiket"),  
    path('tiket/<int:pk>/action-detail', TiketActionView.as_view(), name="detail-action-tiket"),
    path('tiket/<int:pk>/assign', TiketAssignView.as_view(), name="assign-tiket"),
    
    # ================================ TIKET ================================
    path('tiket', TiketListView.as_view(), name="list-tiket"),
    path('new-tiket', TiketCreateView.as_view(), name="create-tiket"), # un-auth page
    path('tiket/<int:pk>/detail', TiketDetailView.as_view(), name="detail-tiket"),
    path('tiket/<int:pk>/update', TiketUpdateView.as_view(), name="update-tiket"),
    path('tiket/<int:pk>/delete', TiketDeleteView.as_view(), name="delete-tiket"),
    
    # ================================ USER ================================
    path('user', UserListView.as_view(), name="user-list"),
    path('user/add', UserCreateView.as_view(), name="user-create"),
    path('user/<int:pk>/edit', UserUpdateView.as_view(), name="user-edit"),
    path('user/<int:pk>/delete', UserDeleteView.as_view(), name="user-delete"),
]
