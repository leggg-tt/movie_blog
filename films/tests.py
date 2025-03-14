from django.test import TestCase
from django.contrib.auth.models import User
from .models import Film, Category, Review, Favorite, ReviewLike


class FilmReviewSystemTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create a movie category
        self.category = Category.objects.create(name='Action')

        # Create a movie
        self.film = Film.objects.create(
            title='Test Movie',
            director='John Doe',
            actors='Actor A, Actor B',
            release_year=2025,
            description='A test movie description.',
            uploader=self.user
        )
        self.film.categories.add(self.category)

    def test_film_creation(self):
        """Test film creation and retrieval"""
        film = Film.objects.get(title='Test Movie')
        self.assertEqual(film.director, 'John Doe')
        self.assertIn(self.category, film.categories.all())

    def test_review_creation_and_rating(self):
        """Test review creation and rating calculation"""
        Review.objects.create(film=self.film, user=self.user, title='Great!', content='Loved it!', rating=5)
        Review.objects.create(film=self.film, user=self.user, title='Okay', content='It was okay.', rating=3)
        self.assertEqual(self.film.average_rating(), 4)  # (5+3)/2 = 4

    def test_favorite_system(self):
        """Test user favoriting a movie"""
        Favorite.objects.create(user=self.user, film=self.film)
        with self.assertRaises(Exception):
            Favorite.objects.create(user=self.user, film=self.film)  # Should trigger unique_together constraint

    def test_review_like_system(self):
        """Test review like functionality"""
        review = Review.objects.create(film=self.film, user=self.user, title='Nice', content='Good movie.', rating=4)
        like = ReviewLike.objects.create(user=self.user, review=review)
        self.assertEqual(review.like_count(), 1)
        with self.assertRaises(Exception):
            ReviewLike.objects.create(user=self.user, review=review)  # Cannot like the same review twice
