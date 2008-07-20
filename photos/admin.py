"""Django-admin-related stuff for the photos application."""
from django.contrib import admin

from obeattie.photos import models as photos_models

class FlickrUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'nsid', 'real_name', 'location', 'is_pro', 'is_flickr_admin', )
    list_display_links = ('username', 'nsid', )
    list_filter = ('is_me', 'is_pro', 'is_flickr_admin', )
    search_fields = ('username', 'nsid', 'real_name', 'location', )
admin.site.register(photos_models.FlickrUser, FlickrUserAdmin)

class PhotosetAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', )
    search_fields = ('title', 'description', )
admin.site.register(photos_models.Photoset, PhotosetAdmin)

class PhotoAdmin(admin.ModelAdmin):
    date_hierarchy = 'posted_timestamp'
    fieldsets = (
        (None, {
            'fields': ('id', 'title', 'description', ),
        }),
        ('Permissions', {
            'fields': ('public_viewable', 'friends_viewable', 'family_viewable', ),
            'description': u'Permissions for this photograph. If the photo is publicly viewable then the friends and family settings will have no effect.',
        }),
        ('Timestamps', {
            'fields': ('posted_timestamp', 'taken_timestamp', 'updated_timestamp', ),
            'description': u'Various dates and times relating to the photograph.',
        }),
        ('Miscellaneous', {
            'fields': ('license', 'rotation_degrees', ),
            'classes': ('collapse', ),
            'description': u'Random bits and pieces.',
        }),
    )
    list_display = ('title', 'posted_timestamp', 'taken_timestamp', 'id', )
    list_display_links = ('title', 'id', )
    list_filter = ('public_viewable', 'friends_viewable', 'family_viewable', 'posted_timestamp', 'taken_timestamp', )
    save_on_top = True
    search_fields = ('title', 'description', 'id', )

class MyPhotoAdmin(PhotoAdmin):
    pass
admin.site.register(photos_models.MyPhoto, MyPhotoAdmin)

class OthersPhotoAdmin(PhotoAdmin):
    def __init__(self, *args, **kwargs):
        # Hack to allow the += (not allowed in the class body...)
        self.list_display += ('owner', 'is_favourite', )
        self.list_filter += ('is_favourite', )
        return super(OthersPhotoAdmin, self).__init__(*args, **kwargs)
admin.site.register(photos_models.OthersPhoto, OthersPhotoAdmin)

class PhotoSizeAdmin(admin.ModelAdmin):
    list_display = ('label', 'photo', 'width', 'height', 'is_flickr', )
    list_filter = ('is_flickr', )
    search_fields = ('label', 'photo__title', 'detail_url', 'location', )
admin.site.register(photos_models.PhotoSize, PhotoSizeAdmin)

class PhotoNoteAdmin(admin.ModelAdmin):
    list_display = ('photo', 'owner', 'text', )
    search_fields = ('text', )
admin.site.register(photos_models.PhotoNote, PhotoNoteAdmin)

class PhotoTagAdmin(admin.ModelAdmin):
    pass
admin.site.register(photos_models.PhotoTag, PhotoTagAdmin)
