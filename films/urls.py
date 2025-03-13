from django.urls import path
from . import views, api_views

urlpatterns = [
    path('', views.film_list, name='film_list'),
    path('film/<int:film_id>/', views.film_detail, name='film_detail'),
    path('film/<int:film_id>/review/', views.add_review, name='add_review'),
    path('category/<str:category_name>/', views.category_films, name='category_films'),
    path('favorite/<int:film_id>/', views.toggle_favorite, name='toggle_favorite'),

    # 数据API
    path('api/ratings-data/', api_views.ratings_data, name='ratings_data'),
    path('api/popular-films-data/', api_views.popular_films_data, name='popular_films_data'),
    path('data-visualization/', views.data_visualization, name='data_visualization'),
    path('review/<int:review_id>/like/', views.toggle_review_like, name='toggle_review_like'),
    path('upload/', views.upload_film, name='upload_film'),
]