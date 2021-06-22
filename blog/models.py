from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import  reverse


'''CREATING CUSTOM OBJECTS'''
# objects (models.objects)is the default manager for every model that retrieves all objects in the database 
# However, on can define custom managers for the models
# Below is a custom manager that retrieves posts with a status='published'
class PublishedManager(models.Manager):
    def get_queryset(self):
        # Fetch the usual queryset returned by the default objects then add a filter to it 
        return super(PublishedManager, self).get_queryset().filter(status='published')


# Create your models here.
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'), ('published', 'Published'),
    )
    title = models.CharField(max_length=200)

    # slug is intended to be used in urls, a slug is a short label containing only letters, numbers...
    # ...Underscores or hyphens. Slug will enable the creation of beautiful, seo friendly urls for blog posts
    # unique_for_date prevents the entry of two records with the same slug and date
    # unique_for_date ensures that there is only one post with a slug for a given date
    # Django prevents multiple posts from having the same slug
    slug = models.SlugField(max_length=250, unique_for_date='publish') # Publish here refers to the publish field

    # Author has a many to one relationship 
    # The field will contain the primary key of the user in the User model 
    # related_name is the name givven to the reverse relationship from User to Post, this enables easy access of related objects
    author = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='blog_posts')

    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True) # auto_now_add, updates with time and date at the creation of the record
    updated = models.DateTimeField(auto_now=True) #  Updates whenever Model.save() is called
    
    # the choices parameter limits us to one of the specified choices
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        # This tells django to sort data beginning with the latest published by default 
        ordering = ('-publish',)
    
    def __str__(self):
        # The default human readable representation of the object 
        return self.title

    #Creating custom managers for the post model   
    objects = models.Manager() # Ths is the default manager, accessed via Post.objects
    published = PublishedManager() # Post.published

    # IF no manager is defined in the model, django automaticaly creates the objects default manager

    def get_absolute_url(self):
        '''
        The canonical url, is the single url that is the main url for a blog post
        setting the canonical url here means that we can refer to it from the templates 
        '''
        return reverse('blog:post_detail', args=[ self.publish.year,
                                                self.publish.month,
                                                self.publish.day,
                                                self.slug ])

class Comment(models.Model):
    '''
    In the post, atribute below there is a related_name atribute
    the related_name atribute allows you to name the relationship from 
    the related object back to this one. For instance 
    you can retrieve the post of a comment using comment.post
    you can retrieve all comments using post.comments.all() instead of post.comment_set.all()
    '''
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)# Creation date 
    updated = models.DateTimeField(auto_now=True)# updated date everytime there is an update
    active = models.BooleanField(default=True)

    # Tell django that whenever comment objects are called, order using created field
    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    
