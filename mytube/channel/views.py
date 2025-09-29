from django.shortcuts import redirect
from django.views.generic import UpdateView
from django.urls import reverse_lazy

from .models import Channel


def create_channel(request):
    if request.user.is_authenticated:
        Channel.objects.create(auther=request.user, name=request.user.username)
        return redirect("account:profile", args=[request.user.pk])
    

class ChannelUpdateView(UpdateView):
    model = Channel
    template_name = "channel/profile.html"
    fields = ["name", "avatar", "banner", "poenitization"]

    def get_success_url(self):
        return reverse_lazy("channel:profile_channel", args=[Channel.objects.get(author=self.request.user).pk])
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["poenitization"].disabled = True
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumbs"] = [
            {"name": "Home", "url": reverse_lazy("content:home")},
            {"name": "User profile", "url": reverse_lazy("account:profile", args=[self.request.user.pk])},
            {"name": "Channel profile", "url": ""},
        ]
        return context 
