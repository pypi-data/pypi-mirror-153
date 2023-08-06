from django.contrib import admin
from reversion.admin import VersionAdmin

from huscy.project_documents import models


@admin.register(models.DocumentType)
class DocumentTypeAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = 'name',


@admin.register(models.Document)
class DocumentAdmin(VersionAdmin, admin.ModelAdmin):
    date_hierarchy = 'uploaded_at'
    list_display = '_project', 'filename', 'document_type', 'uploaded_at', 'uploaded_by'
    list_filter = 'document_type__name',

    def _project(self, document):
        return f'{document.project.local_id_name} {document.project.title}'

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
