from django.contrib import admin
from .models import Profile

#Decorator, register the Profile model to admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    #Define display content
    list_display = ('user', 'bio')
    #Define your search
    search_fields = ('user__username', 'bio')