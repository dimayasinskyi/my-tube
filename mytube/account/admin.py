from django.contrib import admin

from content.models import UserWatchHistory, Recommendations
from .models import CustomUser


class UserWatchHistoryInline(admin.TabularInline):
    model = UserWatchHistory
    extra = 0


class RecommendationsInline(admin.TabularInline):
    model = Recommendations
    extra = 0


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    inlines = [UserWatchHistoryInline, RecommendationsInline]