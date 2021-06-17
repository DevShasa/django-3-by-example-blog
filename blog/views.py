from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import  ListView

# Create your views here.
# Views receive web request and return web response 
# Each view renders a template, passing variables to it

class PostListView(ListView):

    # Default: model = Post
    queryset = Post.published.all()
    # Default: post_list
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, 
                                    status='published', 
                                    publish__year=year, 
                                    publish__month=month, 
                                    publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})


'''This is the old listview, which is similar to PostListView above'''
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# def post_list(request):
#     object_list = Post.published.all() # Here we use our custom object 
#     # Alternatively Post.object.filter(status="published")
#     paginator = Paginator(object_list, 3) # Instantiate paginator class, display three posts on every page
#     page = request.GET.get('page') # Get the page parameter, which indicates current page number
#     try:
#         # Obtain the objects of the desired page by calling page() method of paginator 
#         posts = paginator.page(page)
#     except  PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         # When you  load blog/ this line will be rendered
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is oyut of range, deliver last page of results
#         posts = paginator.page(paginator.num_pages)
#     return render(request, 'blog/post/list.html', {'posts':posts})
