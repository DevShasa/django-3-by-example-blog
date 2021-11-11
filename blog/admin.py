from django.contrib import admin
from .models import Post, Comment, PostImage 
from django.utils.html import format_html


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
class PostImageAdmin(admin.ModelAdmin):
    list_display = ('post_slug', 'thumbnail_tag')
    readonly_fields=('thumbnail',)
    search_fields = ('post__slug',)

    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return format_html(f'<img src="{obj.thumbnail.url}">')
        return "_"
    
    def post_slug(self, obj):
        return obj.post.slug
admin.site.register(PostImage, PostImageAdmin)