from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import  ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

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
    

    # Get the comments listed as active
    comments  = post.comments.filter(active=True)
    # This is a flag used to display whether there is a new comment so that it can be displayed
    new_comment = None 
    # when data is submitted using the form 
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
    
    return render(request,"blog/post/detail.html",
                # Context
                {   
                    "post": post, # The blogpost   
                    "comments": comments, # The comments under the blog
                    "new_comment": new_comment, # The comment just submitted
                    "comment_form": comment_form # The modelForm object
                }
    )


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
