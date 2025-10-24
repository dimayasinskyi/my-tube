from django.urls import path

from .views import ListAdmin, DetailAdmin, register_admin, login_in, logout


app_name = "admin"

urlpatterns = [
    path("", ListAdmin.as_view(), name="admin-list"),
    path("register/", register_admin, name="admin-register"),
    path("login/", login_in, name="login-in"),
    path("logout/", logout, name="logout"),
    path("<str:id>/", DetailAdmin.as_view(), name="admin-detail"),
]