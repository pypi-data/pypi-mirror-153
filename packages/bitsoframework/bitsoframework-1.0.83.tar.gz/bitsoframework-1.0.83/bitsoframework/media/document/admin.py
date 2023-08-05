from django.contrib import admin

from bitsoframework.media.settings import Document


class DocumentAdmin(admin.ModelAdmin):
    model = Document
    list_display = ["id", "title", "filename", "file", "parent_type", "parent_id"]
    search_fields = ["title", "filename"]
