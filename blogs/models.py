#Import Django database model module to provide 0RM mapping function
from django.db import models
#Directly use the built-in user authentication model
from django.contrib.auth.models import User

#blog Tags
LIFESTYLE_CATEGORIES = [
    ('travel', 'Travel'),
    ('food', 'Food'),
    ('health', 'Health & Wellness'),
    ('fitness', 'Fitness'),
    ('reading', 'Reading'),
    ('parenting', 'Parenting'),
    ('finance', 'Personal Finance'),
    ('fashion', 'Fashion & Beauty'),
    ('tech', 'Technology & Gadgets'),
    ('home', 'Home & Living'),
    ('hobbies', 'Hobbies & Crafts'),
    ('career', 'Career & Work'),
    ('relationships', 'Relationships & Love'),
    ('other', 'Other')
]


#Define the Blog model class
class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    #Foreign key association User model, application association mechanism, add reverse relationship
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    #Creation time
    created_at = models.DateTimeField(auto_now_add=True)
    #Update time
    updated_at = models.DateTimeField(auto_now=True)
    #Select Type
    category = models.CharField(max_length=20, choices=LIFESTYLE_CATEGORIES, default='other')
    #Views
    views = models.PositiveIntegerField(default=0)

    @property
    def reading_time(self):
        #Assuming an average reading speed of 200 words per minute
        word_count = len(self.content.split())
        minutes = max(1, round(word_count / 200))
        return minutes

    #Display blog title in admin interface
    def __str__(self):
        return self.title

    #Returns the number of comments at the bottom of the blog
    @property
    def comment_count(self):
        #self.comments引用comment模型中的related_name='comments'
        return self.comments.count()

#Define the Comment model class
class Comment(models.Model):
    #Same as above
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    #Same as above
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comments')
    content = models.TextField()
    #Same as above
    created_at = models.DateTimeField(auto_now_add=True)

    #Display commenter name and blog title in the admin interface
    def __str__(self):
        return f"Comment by {self.user.username} on {self.blog.title}"