from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.contrib.postgres.search import SearchVector


# Create your views here.
# Views receive web request and return web response 
# Each view renders a template, passing variables to it

def post_detail(request, year, month, day, post):

    # Fetch the post 
    post = get_object_or_404(Post, slug=post, 
                                    status='published', 
                                    publish__year=year, 
                                    publish__month=month, 
                                    publish__day=day)
    
    # Fetch the comments 
    comments  = post.comments.filter(active=True)


    # This is a flag used to display whether there is a new comment so that it can be displayed
    new_comment = None 
    # The detail view also includes a form for users to submit comments, the comment form appears as a modal 
    if request.method == 'POST':
        comment_form = CommentForm(data = request.POST)
        if comment_form.is_valid():
            # Create a new comment object but dont save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the post to the comment  
            new_comment.post = post
            # Now we can save  
            new_comment.save()
    else:
        comment_form = CommentForm()
    
    # THE THREE LINES OF CODE BELOW FUNCTION TO RECCOMEND SIMILAR POSTS TO USERS ON DETAILVIEW
    # Get a python [list] of ids of tags for the current post...
    # values_list() queryset returns tuples with the values of the given fields...
    # flat=True is to get the list [1, 2, 3, ...] instead of [(1,), (2,), (3,) ...] 
    post_tag_ids = post.tags.values_list("id", flat=True)
    # Fetch all posts that have the tags in the post_tag_ids queryset
    similar_posts = Post.published.filter(tags__in=post_tag_ids).exclude(id=post.id)
    # Use Count to generate a value that represents number of shared tags
    # Order the results by the number of shared tags in -descending-order...
    # Order the resulting queryset above by published so that recent posts come first...
    # for more info on annotate check page 127 in django documentation book     
    similar_posts = similar_posts.annotate(same_tags =Count("tags")).order_by('-same_tags', "-publish")[:4]

    return render(request,"blog/post/detail.html",
                # Context
                {
                "post": post, # The blogpost   
                "comments": comments, # The comments under the blog
                "new_comment": new_comment, # The comment just submitted
                "comment_form": comment_form, # The modelForm object
                "similar_posts": similar_posts
                }) 
                
# This handles the form 
def post_share(request, post_id):
    '''
    Takes a post and sends it as an email
    '''
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False 
    if request.method == 'POST':
        # If the request is POST this means the user has submitted data 
        form = EmailPostForm(request.POST) # Create a form object
        if form.is_valid():
            # The form has passed the nescesarry validation
            cd = form.cleaned_data
            # Send the email using the form data 
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} reccomends you read blog post: {post.title}"
            message = f"Read {post.title} at {post_url} \n" \
                        f"{cd['name']}'s commented {cd['comments']}"
            
            '''
            send_mail() function takes several parameters 
            > SUBJECT
            > MESSAGE
            > SENDER
            > LIST OF RECEPIENTS 
            > fail_silently = bool
            '''
            send_mail(subject, message, "bigballs@admin.com", [cd['to'], ])
            sent = True
    else:
        # When the view is initialy loaded, create an instance of form 
        # The instance is used to display the empty form
        
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent})


def post_list(request, tag_slug=None):
    object_list = Post.published.all() # Here we use our custom object 
    # Alternatively Post.object.filter(status="published")

    tag = None
    if tag_slug:

        # Fetch the tag from the tag database 
        tag = get_object_or_404(Tag, slug=tag_slug)
        # Get only the posts that have the indicated tag 
        object_list = object_list.filter(tags__in=[tag]) 

    # Instantiate paginator class, display three posts on every page
    paginator = Paginator(object_list, 3) 
    # Get the page parameter, which indicates current page number
    page = request.GET.get('page') 
    try:
        # Obtain the objects of the desired page by calling page() method of paginator 
        posts = paginator.page(page)
    except  PageNotAnInteger:
        # If page is not an integer deliver the first page
        # When you  load blog/ this line will be rendered
        posts = paginator.page(1)
    except EmptyPage:
        # If page is oyut of range, deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(
                    request, 
                    'blog/post/list.html', 
                    {'posts':posts,'tag':tag,}
                )

def post_search(request):
    form = SearchForm()
    query = None
    results = []

    # The user has submitted a request for the resource
    if "query" in request.GET:
        form =  SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query'] # Query is the form field, get its content
            # For more options on search including adding weight to search terms, ordering and word-stem,
            # View django3 by example page 88
            results = Post.published.annotate(search=SearchVector('title','body'),).filter(search=query)
        
    return render(request, 'blog/post/search.html',{'form':form,'query':query,'results':results})


# from django.views.generic import ListView
# class PostListView(ListView):

#     # Default: model = Post
#     queryset = Post.published.all()
#     # Default: post_list
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'