from django.contrib.gis.db import models

from obeattie.generic.tagging.fields import TagField
from obeattie.generic.tagging.models import Tag as GenericTag, TagManager as GenericTagManager
from obeattie.metadata.models import License

class FlickrUser(models.Model):
    """Represents a User on Flickr."""
    nsid = models.CharField('Flickr NSID', max_length=250, blank=False, null=False, primary_key=True)
    # Flags
    is_flickr_admin = models.BooleanField(default=False)
    is_pro = models.BooleanField(default=False)
    # Details
    username = models.CharField(max_length=250, blank=False, null=False)
    real_name = models.CharField(max_length=250, blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)
    is_me = models.BooleanField(default=False, help_text='If this user is me, this should be set.')
    # URLs
    photos_url = models.URLField(blank=False, null=False, verify_exists=False)
    profile_url = models.URLField(blank=False, null=False, verify_exists=False)
    # Flickry metadata
    flickr_icon_farm = models.IntegerField(blank=True, null=True, editable=False)
    flickr_icon_server = models.IntegerField(blank=True, null=True, editable=False)
    
    class Admin:
        pass
    
    def __unicode__(self):
        return self.real_name or self.username

class PhotoTag(GenericTag):
    flickr_id = models.IntegerField('Flickr ID', blank=False, null=False, unique=True, db_index=True)
    owner = models.ForeignKey(FlickrUser, blank=False, null=False)
    # Manager
    objects = GenericTagManager()

class Photoset(models.Model):
    """Represents a Flickr photoset."""
    id = models.IntegerField('Flickr ID', blank=False, null=False, primary_key=True)
    # Metadata
    title = models.CharField(max_length=250, blank=False, null=False, db_index=True)
    description = models.TextField(blank=True, null=True)
    # Flickry metadata
    primary_photo_id = models.IntegerField('Primary Photo ID', blank=True, null=True)
    flickr_secret = models.CharField(max_length=50, blank=True, null=True)
    flickr_server_farm = models.PositiveIntegerField(blank=False, null=False)
    flickr_server = models.PositiveIntegerField(blank=False, null=False)
    
    class Admin:
        pass
    
    def __unicode__(self):
        return self.title

class Photo(models.Model):
    """Base model representing a Flickr photo."""
    id = models.IntegerField('Flickr ID', blank=False, null=False, primary_key=True)
    # Metadata
    title = models.CharField(max_length=250, blank=False, null=False, db_index=True)
    description = models.TextField(blank=True, null=True)
    rotation_degrees = models.IntegerField(blank=False, null=False, default=0)
    license = models.ForeignKey(License, blank=True, null=True)
    location = models.PointField(blank=True, null=True)
    tags = TagField(PhotoTag)
    # Permissions
    public_viewable = models.BooleanField(default=False)
    friends_viewable = models.BooleanField(default=False)
    family_viewable = models.BooleanField(default=False)
    # Timestamps
    posted_timestamp = models.DateTimeField(blank=False, null=False)
    taken_timestamp = models.DateTimeField(blank=True, null=True) # Not required in case of no date
    updated_timestamp = models.DateTimeField(blank=True, null=True)
    # Flickr Crap
    flickr_secret = models.CharField(max_length=250, blank=True, null=True, editable=False)
    flickr_original_secret = models.CharField(max_length=250, blank=True, null=True, editable=False)
    # GeoManager
    objects = models.GeoManager()
    
    class Admin:
        list_display = ('title', 'description', 'public_viewable', 'posted_timestamp', )
        list_filter = ('public_viewable', 'posted_timestamp', 'taken_timestamp', )
        search_fields = ('title', )
    
    class Meta:
        ordering = ('-posted_timestamp', 'title', )

class MyPhoto(Photo):
    """Model for storing photos I own."""
    pass

class OthersPhoto(Photo):
    """Model for storing photos other Flickr users own."""
    owner = models.ForeignKey(FlickrUser, blank=False, null=False)
    is_favourite = models.BooleanField(default=True)

class PhotoSize(models.Model):
    """Represents a size of a Photo from Flickr."""
    photo = models.ForeignKey(Photo, blank=False, null=False)
    label = models.CharField(max_length=250, blank=False, null=False)
    # Size
    width = models.PositiveIntegerField(blank=False, null=False, help_text='(In pixels)', editable=False)
    height = models.PositiveIntegerField(blank=False, null=False, help_text='(In pixels)', editable=False)
    # URLs and paths
    location = models.URLField('Location to the image', blank=True, null=True, verify_exists=False)
    detail_url = models.URLField('Location to a page showing the image', blank=True, null=True, verify_exists=False)
    local_file = models.ImageField('Image File', blank=True, null=True, width_field='width', height_field='height', upload_to='images/photos')
    # Miscellaneous
    is_flickr = models.BooleanField('Flickr size?', default=False, help_text='Set if the size was generated by Flickr.', editable=False)
    
    class Admin:
        list_display = ('label', 'photo', 'width', 'height', 'is_flickr', )
        list_filter = ('is_flickr', )
        search_fields = ('label', 'photo__title', 'detail_url', 'location', )
    
    class Meta:
        unique_together = (('photo', 'label', ), ('photo', 'width', 'height', ), )

class PhotoNote(models.Model):
    """Represents a Note applied to a photo from Flickr."""
    id = models.IntegerField('Flickr ID', blank=False, null=False, primary_key=True)
    photo = models.ForeignKey(Photo, blank=False, null=False)
    owner = models.ForeignKey(FlickrUser, blank=False, null=False)
    x = models.PositiveIntegerField(blank=False, null=False)
    y = models.PositiveIntegerField(blank=False, null=False)
    width = models.PositiveIntegerField(blank=False, null=False)
    height = models.PositiveIntegerField(blank=False, null=False)
    text = models.TextField(blank=False, null=False)
    
    class Admin:
        list_display = ('photo', 'owner', 'text', )
        search_fields = ('text', )
    
    def __unicode__(self):
        return self.text
