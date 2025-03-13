from django import forms
from .models import Blog, Comment

#Define the BlogForm class, inheriting from forms.ModelForm
class BlogForm(forms.ModelForm):
    #Define a nested Meta class to configure the behavior of the Blog model
    class Meta:
        model = Blog
        fields = ['title', 'content', 'category']
        widgets = {
            #Single-line text box
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            #Multi-line text box
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            #Type selection
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

#Define the CommentForm class, inheriting from forms.ModelForm
class CommentForm(forms.ModelForm):
    #Define a nested Meta class to configure the behavior of the Comment model
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            #Multi-line text box, placeholder: placeholder text
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Leave a comment...'})
        }