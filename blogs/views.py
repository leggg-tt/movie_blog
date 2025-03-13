from django.shortcuts import render, redirect, get_object_or_404
#Import login authentication limiter
from django.contrib.auth.decorators import login_required
#Import one-time verification message
from django.contrib import messages
#JSON
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Blog, Comment
from .forms import BlogForm, CommentForm

#Define the blog_list view function
def blog_list(request):
    #Sort by creation time
    blogs = Blog.objects.all().order_by('-created_at')

    #Blog Pagination
    paginator = Paginator(blogs, 10)  # 10 blog posts per page
    page_number = request.GET.get('page')
    #Return to the blog within the specified page
    page_obj = paginator.get_page(page_number)
    #Rendered page: page_obj contains paging information and the blog list of the current page
    return render(request, 'blogs/blog_list.html', {'page_obj': page_obj})

#Define the view function for the blog details page
def blog_detail(request, blog_id):
    #Get the blog by blog_id, if it does not exist, return 404
    blog = get_object_or_404(Blog, id=blog_id)
    #Blog views increased
    blog.views += 1
    blog.save(update_fields=['views'])
    #Get all comments on this blog sorted by time
    comments = blog.comments.all().order_by('-created_at')
    #Empty comment form
    comment_form = CommentForm()
    #Data passed to the template
    context = {
        'blog': blog,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'blogs/blog_detail.html', context)


@login_required #登陆验证器
#Define the view function of create_blog
def create_blog(request):
    if request.method == 'POST':
        #Use submit data to create form data
        form = BlogForm(request.POST)
        if form.is_valid():
            #Not directly saved
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            messages.success(request, 'Blog post published successfully！')
            #Redirect
            return redirect('blog_detail', blog_id=blog.id)
    else:
        form = BlogForm()

    return render(request, 'blogs/create_blog.html', {'form': form})


@login_required
#Define the add_comment view function
def add_comment(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        #Use submit data to create form data
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()

            #If it is an AJAX request (by checking the request headers)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                #Return JSON response to AJAX request
                return JsonResponse({
                    'success': True,
                    'comment_id': comment.id,
                    'username': comment.user.username,
                    'content': comment.content,
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
                })

            messages.success(request, 'Comment added！')
            # Redirect
            return redirect('blog_detail', blog_id=blog.id)
        else:
            #Handling invalid forms
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                #If it is an AJAX request, return an error message
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
            else:
                #For normal requests, add error messages and redirect
                messages.error(request, 'Error adding comment. Please check your input.')
                return redirect('blog_detail', blog_id=blog.id)

    #If it is not a POST request or the form is invalid
    return redirect('blog_detail', blog_id=blog.id)


@login_required
#Define the my_blogs view function
def my_blogs(request):
    #Filter out blogs that match the identity of the user making the request and sort by creation time
    blogs = Blog.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'blogs/my_blogs.html', {'blogs': blogs})
