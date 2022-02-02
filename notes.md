
## Querysets 
A Queryset is a collection of database querries to retrieve objects from the database

```python
> python manage.py shell
>>> from django.contrib.auth.models import User
>>> from blog.models import Post
# get method allows one to retrive a single object from the database
# If no results are returned by the database, the method will raise
# a DoesNotExist exeption 
#
# If the database returns more than one results then it will raise a MultipleOpjectsReturned exeption
>>> user = User.objects.get(username='shasa')

>>> # Create a new post 
# Performs an insert SQL statement 
>>> post = Post(title= "Another post", slug="Another-post", author=user, body="post body")
>>> post.save()
# You can create and save one touch like this 
'''
Post.objects.create(title='One more post',
slug='one-more-post',
body='Post body.',
author=user)
'''
```

each django model gets at leat one manager called objects
to retrieve all objects from a table use the ***all()*** method on the default objects manager
```python
all_posts = Post.objects.all()
>>> for x in all_posts:
        # Print a list of all posts, because no atribute defined will return
        # The __str__ of the model
...     print(x)

```

To filter a queryset use the ***filter()*** method on the manager
```python
# ONly get the entries that have "post" in their title
Post.objects.filter(title__contains="post")
>>> for x in filtered:
...     print(x)
... 
Third blog post
Second post
First post

# ONly get the entries published in 2021
Post.objects.filter(publish__year=2020)

# Filter using multiple fields 
Post.objects.filter(title__contains="post", status = 'draft')
>>> for x in filtered:
...     print(x)
... 
Second post
First post
```

> Querries with field lookup methods are built using two underscores for example ***publish__year***, the same notation is also used for accesing fields of related models such as ***author_username='shasa'***

You can exclude certain results from the queryset using the ***exlude*** method of the manager
```python
# Fetch all posts published in 2021,exlude titles that dont start with why 
>>> for x in Post.objects.filter(publish__year=2021).exclude(title__startswith='Why'):
...     print(x)
... 
New Title
Third blog post
Second post
First post
>>> 
```

```python
# Exclude all posts that have status="draft"
>>> for x in Post.objects.exclude(status='draft'):
...     print(x)
... 
Third blog post
```

You can order results by different fields using ***order_by()*** method of the manager
```python
Post.objects.order_by('title')
#Indicate descending order
Post.objects.order_by('-title')
```
deleting objects 
```python
post = post.objects.get(id=1)
post.delete()
```

## When querysets are evaluated
creating a queryset does not involve any database activity untill it is evaluated. When a queryset is evaluated, it turns into an sql querry to teh database

Querysets are only evaluated if
* The first time one iterates over them
* When they are sluced
* When they are pickled or cathed
* when you call ***repr()*** or ***len()*** on them
* when you explicitly call ***list()*** o them 
* when you test them in a statement such as bool() , or , and , or if

# Create a custom manager
The custom manager only returns items that have status="published"
```python
class PublishedManager(models.Manager):
    def get_queryset(self):
        # Fetch the usual queryset returned by the default objects then add a filter to it 
        return super(PublishedManager, self).get_queryset().filter(status='published')
```
And then made this addition at the bottom of Posts(models.Model)
```python
#Creating custom managers for the post model
objects = models.Manager() # Ths is the default manager, accessed via Post.objects
published = PublishedManager() # Post.published
```

Now we can run the query
```python
>>> from blog.models import Post
>>> for x in Post.published.all():
...     print(x)
... 
Third blog post
>>> 

```

# Reverse relationships
Say you have a model Category and a model Product, each product field 
has a category foreign key, many products can have one category. 
the foreign key has related name "products"

getting the reverse relationship list all products attached to a category

```python
>> from shop.models import Category, Products
>> cat = Category.objects.all()
>> for x in cat:
        print(x, ": ",products.all())
```
RESULT 
```
Home Improvement:  <QuerySet [<Product: Pliers>]>
foodstuffs:  <QuerySet [<Product: Green Tea>, <Product: Sugar>]>
```
GET ALL RELATED OBJECTS BY NAME
```python
>>> for x in cat:
...     for i in x.products.all():
...             print(x,": ", i.name)
... 
Home Improvement :  Pliers
foodstuffs :  Green Tea
foodstuffs :  Sugar
```
