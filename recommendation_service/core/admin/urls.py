from django.urls import path

from .views import ListAdmin, DetailAdmin, register_admin


app_name = "admin"

urlpatterns = [
    path("", ListAdmin.as_view(), name="admin-list"),
    path("register/", register_admin, name="admin-register"),
    path("<str:id>/", DetailAdmin.as_view(), name="admin-detail"),
]