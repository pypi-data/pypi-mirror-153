from django.contrib import admin
from easy_thumbnails.models import Source, Thumbnail

from bitsoframework.media.settings import Image


class ImageAdmin(admin.ModelAdmin):
    model = Image
    list_display = ["id", "title", "filename", "file", "parent_type", "parent_id", "width", "height"]
    search_fields = ["title", "filename"]


class ThumbnailAdmin(admin.TabularInline):
    model = Thumbnail


class SourceAdmin(admin.ModelAdmin):
    model = Source
    list_display = ("id", "storage_hash", "modified")
    inlines = (
        ThumbnailAdmin,
    )


admin.site.register(Source, SourceAdmin)
