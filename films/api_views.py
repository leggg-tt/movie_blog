from django.http import JsonResponse
from django.db.models import Count
from .models import Film, Review

#Get the rating view
def ratings_data(request):
    """Get rating distribution data"""
    #Get the rating distribution from the review model, count the number of each rating, and sort by rating
    ratings = Review.objects.values('rating').annotate(count=Count('rating')).order_by('rating')
    #Convert to the format required by the front end
    data = [0, 0, 0, 0, 0]  #Initialize 1-5 star rating count
    for item in ratings:
        #Use score-1 as index to access the corresponding quantity position in the array
        data[item['rating'] - 1] = item['count']
    #Return jason data
    return JsonResponse({'ratings': data})

#Get the most popular movie views
def popular_films_data(request):
    #Get all movie objects and add the reviews_count field to each movie to count the number of reviews corresponding to each film model, in descending order
    films = Film.objects.annotate(reviews_count=Count('reviews')).order_by('-reviews_count')[:10]
    #Create dictionary, data format, labels: data
    data = {
        'labels': [film.title for film in films],
        'data': [film.reviews_count for film in films]  #Use new name
    }
    #Return jason data
    return JsonResponse(data)