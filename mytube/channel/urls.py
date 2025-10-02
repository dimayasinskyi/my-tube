from django.urls import path

from .views import create_channel, delete_channel, ChannelUpdateView


app_name = "channel"

urlpatterns = [
    path("create/", create_channel, name="create_channel"),
    path("delete/", delete_channel, name="delete_channel"),
    path("profile/<int:pk>/", ChannelUpdateView.as_view(), name="profile_channel")
]