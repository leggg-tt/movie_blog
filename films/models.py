from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


#Movie Classification Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    #Define the background display
    def __str__(self):
        return self.name
    #Specifying plural names
    class Meta:
        verbose_name_plural = "Categories"

#Movie Model
class Film(models.Model):
    title = models.CharField(max_length=200)
    director = models.CharField(max_length=200)
    actors = models.TextField()
    release_year = models.IntegerField()
    poster = models.ImageField(upload_to='posters/', blank=True)
    categories = models.ManyToManyField(Category)
    description = models.TextField()
    #Joint responsibility mechanism
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_films')\
    #Automatically add creation time
    created_at = models.DateTimeField(auto_now_add=True)
    #Display movie name in the background
    def __str__(self):
        return self.title

    #Calculate average movie score
    def average_rating(self):
        #Get all movie reviews
        reviews = self.reviews.all()
        #Calculate the average of the ratings
        #Check if reviews is empty
        if reviews:
            #Use the aggregate() method to calculate the average of the rating field of reviews
            result = self.reviews.aggregate(avg=Avg('rating'))['avg']
            return result if result is not None else 0
            #return sum(review.rating for review in reviews) / len(reviews)
        return 0
    #Count the number of reviews for a movie
    @property
    def review_count(self):
        return self.reviews.count()

#Movie review model
class Review(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='film_reviews')
    title = models.CharField(max_length=200)
    content = models.TextField()
    #Let rating only select non-negative integers from 1 to 5
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #Calculate likes
    def like_count(self):
        return self.likes.count()
    #Display movie review title-movie title in the background
    def __str__(self):
        return f"{self.title} - {self.film.title}"

#Favorite movie model
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        #Limit the same user from liking a movie twice
        unique_together = ('user', 'film')

    def __str__(self):
        #The background shows the username and her favorite movies
        return f"{self.user.username} favorited {self.film.title}"

#Movie review like model
class ReviewLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_likes')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        #Ensure that a user can only like a comment once
        unique_together = ('user', 'review')
    #Define the background display
    def __str__(self):
        return f"{self.user.username} liked {self.review.title}"
