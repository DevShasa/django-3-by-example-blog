'''
This file is used to generate sitemap using the content in the database
'''
from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        # Django will retrieve each post's absoute url
        return Post.published.all()

    def lastmod(self, obj):
        '''
        retrieves each object returned by items() above and returns 
        the last time that object was modified
        '''
        return obj.updated 