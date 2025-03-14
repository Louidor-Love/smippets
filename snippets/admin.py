from django.contrib import admin

from .models import Language,Snippet,UserProfile


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "language", "public", "created")
    list_filter = ("public", "language", "created")
    search_fields = ("name", "description", "snippet")

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "slug")
    search_fields = ("user__username",)
    readonly_fields = ('slug',)   