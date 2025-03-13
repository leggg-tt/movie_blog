from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('create/', views.create_blog, name='create_blog'),

    #'/5/'-views.blog_detail(request, blog_id=5)
    path('<int:blog_id>/', views.blog_detail, name='blog_detail'),

    #同上
    path('<int:blog_id>/comment/', views.add_comment, name='add_comment'),
    path('my-blogs/', views.my_blogs, name='my_blogs'),
]