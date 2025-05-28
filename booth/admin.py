from django.contrib import admin

from .models import Creator
from .tasks import convert_video_to_mp4


@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("id", "name")
    readonly_fields = ("id", "video_mp4", "created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        # Check if this is an update and if the video field has changed
        video_changed = False
        old_video_mp4 = None

        if change:  # This is an update, not a new creation
            # Get the original object from the database
            try:
                original_obj = Creator.objects.get(pk=obj.pk)
                # Compare the video field
                if original_obj.video != obj.video:
                    video_changed = True
                    old_video_mp4 = original_obj.video_mp4
            except Creator.DoesNotExist:
                # Object doesn't exist yet, treat as new
                video_changed = True
        else:
            # This is a new object creation
            video_changed = bool(obj.video)

        # If video changed, clear the existing normalized video
        if video_changed and old_video_mp4:
            # Delete the old MP4 file from storage
            if old_video_mp4:
                old_video_mp4.delete(save=False)
            # Clear the video_mp4 field
            obj.video_mp4 = None

        # Save the object first
        super().save_model(request, obj, form, change)

        # Trigger the video conversion task if video changed
        if video_changed and obj.video:
            convert_video_to_mp4.delay(obj.id)
