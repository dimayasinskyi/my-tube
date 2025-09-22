from django.urls import path

from .views import create_recommendation


urlpatterns = [
    path("", create_recommendation)
]