from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from mytube.celery import create_recommendation
from .models import Recommendations, Video, Tag, UserWatchHistory
from .serializers import VideoSerializer
from .forms import VideoCreateForm, VideoCommentCreateForm


class Home(ListView):
    """Recommendations page if the user is registered, if not a selection of random videos."""
    template_name = "content/home.html"
    context_object_name = "videos"
    paginate_by = 16
    
    def get_videos(self, video):
        """Filters and order videos by parameters in requests."""
        param = self.request.GET
        if param.get("search"):
            videos = video.filter(title__icontains=param.get("search")).order_by("title")
        elif param.get("tag"):
            videos = video.filter(tags=param.get("tag")).order_by("tags")
        else:
            videos = video.order_by("-created_at")
        return videos

    def get_queryset(self):
        """
        If any search parameters are passed that have been processed by the get_videos method,
        it simply returns them or, if the user is not authorized, otherwise shows personalized
        recommendations for the user and creates a task to update them.
        """
        user = self.request.user

        if (self.request.GET.get("search") or self.request.GET.get("tag")) or not user.is_authenticated:
            return self.get_videos(Video.objects.all())[:50]

        serializer = VideoSerializer(self.get_videos(Video.objects.all()), many=True, context={"user": user})
        recommendations = Recommendations.objects.get(user=user).video.all()
        create_recommendation(user, serializer)
        return recommendations
        
    def get_context_data(self, **kwargs):
        """Creates a parameter for page pagination."""
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all().order_by("title")
        
        querystring = self.request.GET.copy()
        if "page" in querystring:
            del querystring["page"]

        context["querystring"] = f"&{querystring.urlencode()}" if querystring else ""
        return context


class VideoCreateView(LoginRequiredMixin, CreateView):
    """Presenting a form VideoCreateForm for creating a video"""
    model = Video
    form_class = VideoCreateForm
    template_name = "content/create_video.html"

    def get_success_url(self):
        return reverse("account:profile", args=[self.request.user.pk])

    def form_valid(self, form):
        """Transfers the feed automatically to the form."""
        form.instance.channel = self.request.user.channel
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Breadcrumb navigation."""
        context = super().get_context_data(**kwargs)

        context["breadcrumbs"] = [
            {"name": "Home", "url": reverse("content:home")},
            {"name": "User profile", "url": reverse("account:profile", args=[self.request.user.pk])},
            {"name": "Channel profile", "url": reverse("channel:profile_channel", args=[self.request.user.channel.pk])},
            {"name": "Create video", "url": ""}
            ]
        return context 
    

class VideoDetailView(DetailView):
    model = Video
    template_name = "content/video_detail.html"

    def get_context_data(self, **kwargs):
        """Adds two variables to the context: ["rec_videos", "liked", "form"]"""
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            serializer = VideoSerializer(Video.objects.all(), many=True, context={"user": user})
            rec_video = Recommendations.objects.get(user=user).video.order_by("?")[:10]
            create_recommendation(user, serializer)
            video_liked = UserWatchHistory.objects.get(user=user, video=self.get_object()).liked
        else:
            rec_video = Video.objects.order_by("?")[:10]
            video_liked = None
        
        context["rec_videos"] = rec_video
        context["liked"] = video_liked
        context["form"] = VideoCommentCreateForm()
        return context
    
    def get_object(self, *args, **kwargs):
        video = super().get_object(*args, **kwargs)
        user = self.request.user
        if user.is_authenticated:
            UserWatchHistory.objects.add_video(video=video, user=user)
        return video 
    
    def post(self, request, *args, **kwargs):
        """Takes a value from a form and calls appropriate actions on the value."""
        video = self.get_object()
        user = request.user

        if user.is_authenticated:
            action = request.POST.get("action")
            if action == "like":
                video.user_like(user=request.user)
            elif action == "dislike":
                video.user_dislike(user=request.user)
            else:
                form = VideoCommentCreateForm(request.POST)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.author = user
                    comment.video = video
                    comment.save()

            return redirect("content:view_video", pk=video.pk)
        return redirect(f"{reverse('account:login')}?next={reverse('content:view_video', args=[video.pk])}")