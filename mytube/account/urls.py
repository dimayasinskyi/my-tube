from django.urls import path

from .views import AthenticationView, ProfileUpdateView, log_out


app_name = "account"

urlpatterns = [
    path("login/", AthenticationView.as_view(), name="login"),
    path("profile/<str:pk>/", ProfileUpdateView.as_view(), name="profile"),
    path("log_out/", log_out, name="log_out")
]