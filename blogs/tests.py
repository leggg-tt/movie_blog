from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Blog, Comment

class BlogViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.blog = Blog.objects.create(title='Test Blog', content='Test Content', user=self.user)

    def test_blog_list_view(self):
        """Test blog list pagination"""
        response = self.client.get(reverse('blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/blog_list.html')

    def test_blog_detail_view(self):
        """Test blog detail page loading and verify view count increment"""
        initial_views = self.blog.views
        response = self.client.get(reverse('blog_detail', args=[self.blog.id]))
        self.blog.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.blog.views, initial_views + 1)

    def test_add_comment_view(self):
        """Test adding a comment"""
        response = self.client.post(reverse('add_comment', args=[self.blog.id]), {'content': 'Nice blog!'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(blog=self.blog, content='Nice blog!').exists())

    def test_my_blogs_view(self):
        """Test the current user's blog management page"""
        response = self.client.get(reverse('my_blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/my_blogs.html')
