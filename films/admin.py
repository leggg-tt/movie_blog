from django.contrib import admin
from .models import Category, Film, Review, Favorite, ReviewLike

#Registered Movie Categories
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    #Define the background display
    list_display = ('name',)
    #Define background search
    search_fields = ('name',)

#Registered Movie Model
@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    #Define the background display
    list_display = ('title', 'director', 'release_year', 'created_at')
    #Defining background filters
    list_filter = ('categories', 'release_year')
    #Defining background searches
    search_fields = ('title', 'director', 'description')
    #Horizontal filter
    filter_horizontal = ('categories',)

#Registered movie review model
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    #Define the background display
    list_display = ('title', 'film', 'user', 'rating', 'created_at')
    #Defining background filters
    list_filter = ('rating', 'created_at')
    #Defining background searches
    search_fields = ('title', 'content', 'film__title', 'user__username')

#Register user collection model
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    #Define the background display
    list_display = ('user', 'film', 'created_at')
    #Defining background filters
    list_filter = ('created_at',)
    #Defining background searches
    search_fields = ('user__username', 'film__title')

#Registered movie review like model
@admin.register(ReviewLike)
class ReviewLikeAdmin(admin.ModelAdmin):
    #Define the background display
    list_display = ('user', 'review', 'created_at')
    #Defining background filters
    list_filter = ('created_at',)
    #Defining background searches
    search_fields = ('user__username',)