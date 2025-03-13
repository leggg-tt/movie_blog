from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg, Count
from django.core.paginator import Paginator
from .models import Film, Category, Review, Favorite, ReviewLike
from .forms import ReviewForm, FilmUploadForm
from blogs.models import Blog

#Movie list page
def film_list(request):
    #Get all movie information, calculate the average score of each group of movies, and sort them in descending order
    films = Film.objects.all().annotate(avg_rating=Avg('reviews__rating')).order_by('-created_at')
    #Get all movie categories
    categories = Category.objects.all()

    #Carousel resource allocation, showing the latest six
    latest_films = Film.objects.all().order_by('-created_at')[:6]

    #Get the highest rated movies
    top_rated_films = Film.objects.annotate(avg_rating=Avg('reviews__rating')) \
                          .filter(avg_rating__isnull=False) \
                          .order_by('-avg_rating')[:6]

    #Get the latest blog
    latest_blogs = Blog.objects.all().order_by('-created_at')[:3]

    #Movie Category Filter
    category_id = request.GET.get('category')
    year = request.GET.get('year')

    if category_id:
        films = films.filter(categories__id=category_id)

    if year:
        films = films.filter(release_year=year)

    #Pagination
    #Maximum 12 per page
    paginator = Paginator(films, 12)
    #Get page number
    page_number = request.GET.get('page')
    #Paging
    page_obj = paginator.get_page(page_number)

    #Get the different release years of all movies in the database
    years = Film.objects.values_list('release_year', flat=True).distinct().order_by('-release_year')

    #Data required by the front end
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'years': years,
        'selected_category': category_id,
        'selected_year': year,
        'latest_films': latest_films,
        'top_rated_films': top_rated_films,
        'latest_blogs': latest_blogs
    }
    return render(request, 'films/film_list.html', context)

#Movie Details
def film_detail(request, film_id):
    #film = get_object_or_404(Film, id=film_id)
    #获取该电影所有影评,以降序排列
    #reviews = film.reviews.all().order_by('-created_at')
    #Get the movie object
    film = get_object_or_404(
        Film.objects.prefetch_related('reviews__likes'),
        id=film_id
    )
    #Get all the reviews for this movie, sorted in descending order
    reviews = film.reviews.all().order_by('-created_at')


    #Check if the user has favorited the movie and the comment like status
    #Negative by default
    is_favorite = False
    if request.user.is_authenticated:
        #Check if it complies
        is_favorite = Favorite.objects.filter(user=request.user, film=film).exists()

        #Add an attribute to each comment indicating whether the user liked it
        for review in reviews:
            #Check if the current user has liked the comment
            review.is_liked_by_user = review.likes.filter(user=request.user).exists()
            #Calculate the total number of likes for a comment
            review.like_count = review.likes.count()
    else:
        #For users who are not logged in, set the default like status
        for review in reviews:
            review.is_liked_by_user = False
            review.like_count = review.likes.count()

    #Rating form, rendering movie details page
    form = ReviewForm()
    #Data required by the front end
    context = {
        'film': film,
        'reviews': reviews,
        'form': form,
        'is_favorite': is_favorite
    }
    return render(request, 'films/film_detail.html', context)

#Login Authenticator
@login_required
#Add Comment View
def add_review(request, film_id):
    film = get_object_or_404(Film, id=film_id)

    if request.method == 'POST':
        #Generate a form
        form = ReviewForm(request.POST)
        if form.is_valid():
            #Do not save by default
            review = form.save(commit=False)
            review.film = film
            review.user = request.user
            review.save()

            #If it is an AJAX request
            #Check the head
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                avg_rating = film.average_rating()
                return JsonResponse({
                    'success': True,
                    'average_rating': avg_rating,
                    'review_count': film.review_count
                })
            #Normal request
            messages.success(request, 'Comment added！')
            return redirect('film_detail', film_id=film.id)
    else:
        form = ReviewForm()

    return render(request, 'films/add_review.html', {'form': form, 'film': film})

#Categorized Movies View
def category_films(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    #Get the corresponding movies according to the category name and calculate the average score of each movie
    films = Film.objects.filter(categories=category).annotate(avg_rating=Avg('reviews__rating'))
    #context variables passed to templates
    context = {
        'category': category,
        'films': films,
    }
    return render(request, 'films/category_films.html', context)

#Login Authenticator
#Favorite Movie View
@login_required
def toggle_favorite(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    #Check if it exists, delete it if it does, create one if it doesn't
    favorite, created = Favorite.objects.get_or_create(user=request.user, film=film)
    #If it already exists, delete it
    if not created:
        favorite.delete()
        is_favorite = False
        messages.success(request, 'Removed from favorites')
    else:
        is_favorite = True
        messages.success(request, 'Added to favorites')

    #If it is an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'is_favorite': is_favorite
        })

    return redirect('film_detail', film_id=film.id)

#Data visualization view
def data_visualization(request):
    return render(request, 'films/data_visualization.html')

#Calculate the average rating (seems not used)
def average_rating(self):
    reviews = self.reviews.all()
    if reviews:
        return sum(review.rating for review in reviews) / len(reviews)
    return 0

#Count the number of movie reviews (not used)
@property
def review_count(self):
    return self.reviews.count()

#Like movie review view
@login_required
def toggle_review_like(request, review_id):
    #Get movie reviews
    review = get_object_or_404(Review, id=review_id)
    #If ReviewLike exists, get it; otherwise create it
    like, created = ReviewLike.objects.get_or_create(user=request.user, review=review)
    #If it already exists, delete it (cancel the like)
    if not created:
        like.delete()
        is_liked = False
    else:
        is_liked = True

    #AJAX request handling
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'is_liked': is_liked,
            'like_count': review.like_count()
        })

    #Normal request redirection
    return redirect('film_detail', film_id=review.film.id)

#Upload Movie View
@login_required
def upload_film(request):
    if request.method == 'POST':
        #Create an instance and pass in the data and files uploaded by the user
        form = FilmUploadForm(request.POST, request.FILES)
        if form.is_valid():
            #Don't save yet
            film = form.save(commit=False)
            #Uploader
            film.uploader = request.user
            film.save()
            form.save_m2m()  #保存多对多关系（类别）
            messages.success(request, 'Movie uploaded successfully! Thank you for your contribution.')
            return redirect('film_detail', film_id=film.id)
    else:
        #Empty form
        form = FilmUploadForm()

    return render(request, 'films/upload_film.html', {'form': form})
