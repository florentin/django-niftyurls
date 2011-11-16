import datetime
from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class BasicModel(models.Model):
    is_published = models.BooleanField(default=True, help_text=_('This object is enabled.'))
    is_featured = models.BooleanField(default=False, help_text=_('This object is special.'))
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True, db_index=True)

    class Meta(object):
        abstract = True

    
class Source(BasicModel):
    """
    A source is a general news source, like CNN, who may provide multiple feeds.
    """
    title = models.CharField(max_length=255)
    #slug = models.SlugField(max_length=255, editable=False)
    link = models.URLField()
    description = models.TextField(blank=True)
    logo = models.ImageField(blank=True, upload_to='images/logos')
    
    class Meta(object):
        ordering = ('title',)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Feed, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return u'%s' % self.title


class Feed(BasicModel):
    """
    A feed is the actual RSS/Atom feed that will be downloaded.  It has a
    many-to-many relationship to categories through the FeedCategoryRelationship
    model, which allows white-lists to be applied to the feed before articles
    will be added to the category.
    """
    title = models.CharField(max_length=255)
    link = models.URLField(unique=True)
    page_url = models.URLField(blank=True, null=True)
    description = models.TextField()
    pubdate = models.DateTimeField(blank=True, null=True)
    source = models.ForeignKey(Source, blank=True, null=True)
    sites = models.ManyToManyField(Site)
    last_downloaded = models.DateTimeField(auto_now=True)
    
    class Meta(object):
        ordering = ('title',)
    
    def __unicode__(self):
        return u'%s - %s' % (self.source.title, self.title)

class Entry(BasicModel):
    guid = models.CharField(max_length=255, blank=True, editable=False, db_index=True)
    title = models.CharField(max_length=255)
    link = models.URLField()
    description = models.TextField()
    pubdate = models.DateTimeField(blank=True, null=True)
    feed = models.ForeignKey(Feed) #, related_name='entries'
    
    class Meta(object):
        ordering = ('-is_published', '-pubdate', 'title')
    
    def __unicode__(self):
        return u'%s' % self.title
    
    def get_absolute_url(self):
        return self.link


class MetaData(models.Model):
    key = models.CharField(max_length=50)
    value = models.TextField()

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    def __unicode__(self):
        return u'key:%s, object_id:%d' % (self.key, self.object_id)