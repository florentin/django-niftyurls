from django.contrib import admin
from models import Source, Feed, Entry, MetaData

class FeedAdmin(admin.ModelAdmin):
    #prepopulated_fields = {"slug": ("title",)}
    pass

class EntryAdmin(admin.ModelAdmin):
    #date_hierarchy = 'date'
    list_display = ('title', 'feed')
    search_fields = ['title', 'description']

admin.site.register(Source)
admin.site.register(Feed, FeedAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(MetaData)
