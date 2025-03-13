#Import the admin module
from django.contrib import admin
#Import the Blog and Comment models
from .models import Blog, Comment

#Register the Blog model to the admin site and define its display format
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'views', 'reading_time', 'created_at', 'updated_at')
    list_filter = ('created_at','updated_at','category')
    search_fields = ('title', 'content', 'user__username')

#Register the Comment model to the admin site and define its display format
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username', 'blog__title')