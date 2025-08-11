from django.contrib import admin
from .models import Announcement
# Register your models here.

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'message')
    list_filter = ('title',)
    search_fields = ('title',)
admin.site.register(Announcement, AnnouncementAdmin)
