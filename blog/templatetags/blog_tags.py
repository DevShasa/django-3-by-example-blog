# Create a simple tag to retrieve teh total post published on the blog 
# Remember to restart the development server after creating a new tag 
from django import template
from ..models import Post 

# This is nescesarry for the tag to be a valid tag library
register = template.Library()

@register.simple_tag # Register the function as a simple tag 
def total_posts():
    '''
    total_posts will be the tag name
    '''
    return Post.published.count() 

# Using an inclusion tag to render an entire template ...
# Using context variables returned by the template tag
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {
        'latest_posts': latest_posts
    }