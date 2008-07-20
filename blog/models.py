from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from obeattie.blog.managers import PostManager
from obeattie.generic.tagging.fields import TagField
from obeattie.metadata.models import Category

class Post(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False)
    slug = models.SlugField(unique=True, blank=True, null=False, prepopulate_from=('title', ))
    # Metadata
    published = models.DateTimeField(blank=False, null=False)
    author = models.ForeignKey(User, blank=False, null=False)
    is_public = models.BooleanField(default=False, help_text=_(u'Whether or not the entry is publically viewable'))
    categories = models.ManyToManyField(Category, blank=True, null=True, related_name='blog_post_set')
    tags = TagField(blank=True, null=True)
    # The post
    intro = models.TextField(_(u'introduction'), blank=False, null=False, help_text=_(u'Use Markdown to add formatting'))
    body = models.TextField(_(u'post body'), blank=True, null=True, help_text=_(u'Use Markdown to add formatting'))
    # Manager
    objects = PostManager()
    
    class Admin:
        date_hierarchy = 'published'
        list_display = ('title', 'published', 'is_public', 'author', )
        list_filter = ('published', 'author', 'is_public', 'categories', )
        search_fields = ('title', 'slug', 'intro', )
    
    def __unicode__(self):
        return self.title

class PostAdmin(admin.ModelAdmin):
    pass
