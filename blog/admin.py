from django.contrib import admin
from .models import Post, Comment

# Register your models here.
@admin.register(Post) # this decorator is similar to admin.site.register()
class PostAdmin(admin.ModelAdmin):
    # The list to display 
    list_display = ('title', 'slug', 'author', 'publish', 'status', 'id')

    # Creates a right sidebar that allows one to filter results by the fields included below 
    list_filter = ('status', 'created', 'publish', 'author')

    # Makes a search bar appear that is searchable using the fields indicated below
    search_fields = ('title', 'body')

    # When one fills in the title field, the slug fiels will prepopulate
    prepopulated_fields = {'slug': ('title',)}

    # Display author field with a lookup widget, this scales much better than a drop down input
    # For instance if you have thousands of users
    raw_id_fields = ('author',)

    # Creates navigation links to navigate through the date hierarchy 
    date_hierarchy = 'publish'

    # Order posts by status and publihs colums by dfault, ordering sets the default ordering criteria
    ordering = ('status', 'publish')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

'''
We are telling django that the model is registered using a custom class that inherits from ModelAdmin
Using the custom class, we can include information on how to display the model an interact with it 
'''