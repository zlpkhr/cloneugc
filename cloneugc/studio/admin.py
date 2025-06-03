from django.contrib import admin

from .models import Ugc


@admin.register(Ugc)
class UgcAdmin(admin.ModelAdmin):
    list_display = ("id", "creator", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("id", "creator__name")
    readonly_fields = ("id", "created_at", "updated_at")

    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False
