from django.shortcuts import redirect
from django.views.generic import UpdateView
from django.urls import reverse_lazy

from .models import Channel
from .forms import ChannelForm


def create_channel(request):
    """Creates a channel for the user."""
    if request.user.is_authenticated:
        Channel.objects.create(author=request.user, name=request.user.username)
        return redirect("account:profile", pk=request.user.pk)


def delete_channel(request):
    """Deletes a user's channel."""
    if request.user.is_authenticated:
        Channel.objects.get(author=request.user).delete()
        return redirect("account:profile", pk=request.user.pk)
    

class ChannelUpdateView(UpdateView):
    """Transfers form ChannelForm."""
    model = Channel
    form_class = ChannelForm
    template_name = "channel/profile.html"

    def get_success_url(self):
        return reverse_lazy("channel:profile_channel", args=[Channel.objects.get(author=self.request.user).pk])
    
    def get_form(self, form_class=None):
        """Makes the poenitization field read-only."""
        form = super().get_form(form_class)
        form.fields["poenitization"].disabled = True
        return form

    def get_context_data(self, **kwargs):
        """Breadcrumb navigation."""
        context = super().get_context_data(**kwargs)

        context["breadcrumbs"] = [
            {"name": "Home", "url": reverse_lazy("content:home")},
            {"name": "User profile", "url": reverse_lazy("account:profile", args=[self.request.user.pk])},
            {"name": "Channel profile", "url": ""},
        ]
        return context 
