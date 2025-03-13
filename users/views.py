from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from films.models import Favorite

#Create a user registration view
def register(request):
    if request.method == 'POST':
        #Create a form and fill it with input data
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created, you can now log in!')
            return redirect('login')
    else:
        #Empty form
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

#Login Authenticator
@login_required
def profile(request):
    return render(request, 'users/profile.html')

#Create and modify personal information view
@login_required
def edit_profile(request):
    if request.method == 'POST':
        #Update the user form of Django_user to modify the email address and username
        u_form = UserUpdateForm(request.POST, instance=request.user)
        #Update personal profile form, used to modify personal profile, avatar
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        #Just load personal information
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    #Passing data to the front end
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/edit_profile.html', context)


@login_required
def favorites(request):
    #Optimize associated queries to reduce the number of database queries
    favorites = Favorite.objects.filter(user=request.user).select_related('film')
    return render(request, 'users/favorites.html', {'favorites': favorites})
