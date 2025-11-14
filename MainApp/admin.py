from django.contrib import admin
from MainApp.models import Comment, Snippet

# Register your models here.
# admin.site.register([Snippet, Comment])

@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ["name", "lang", "creation_date", "public", "code"]
    list_filter = ["name", "creation_date"]
    ordering = ["creation_date"]
    search_fields = ["name", "code"]

@admin.register(Comment)
class SCommentAdmin(admin.ModelAdmin):
    list_display = ["text"]
    search_fields = ["text"]
