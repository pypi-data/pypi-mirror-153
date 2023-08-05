from django.contrib import admin

from bitsoframework.media.settings import CloudDocument


class CloudDocumentAdmin(admin.ModelAdmin):
    model = CloudDocument
    list_display = ["id", "title", "origin_url", "origin_type"]
    search_fields = ["title", "origin_url", "origin_type"]
