from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.
# Views receive web request and return web response 
# Each view renders a template, passing variables to it

def post_list(request):
    posts = Post.published.all() # Here we use our custom object 
    # Alternatively Post.object.filter(status="published")
    return render(request, 'blog/post/list.html', {'posts':posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, 
                                    status='published', 
                                    publish__year=year, 
                                    publish__month=month, 
                                    publish__dau=day)
    return render(request, 'blog/post/detail.html', {'post': post})