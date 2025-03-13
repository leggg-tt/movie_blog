from django import forms
from .models import Review, Film

#Create a movie review form
class ReviewForm(forms.ModelForm):
    #Specifying the review model
    class Meta:
        model = Review
        #Defining the form content
        fields = ['title', 'content', 'rating']
        widgets = {
            #Text Box
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            #Multi-line input
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            #Hide the rating field, we will replace it with a custom star UI
            'rating': forms.HiddenInput(attrs={'id': 'id_rating_hidden'})
        }

#Creating a Movie Upload Form
class FilmUploadForm(forms.ModelForm):
    #Specify film model
    class Meta:
        model = Film
        #Define the form to display content, title, director, actor, year, poster, type, description
        fields = ['title', 'director', 'actors', 'release_year', 'poster', 'categories', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'director': forms.TextInput(attrs={'class': 'form-control'}),
            'actors': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Separate actors with commas'}),
            'release_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'poster': forms.FileInput(attrs={'class': 'form-control'})
        }