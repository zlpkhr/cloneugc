from django.contrib import admin

from .models import Creator
from .tasks import convert_video_to_mp4, create_voice_clone


@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    change_form_template = "admin/booth/creator/change_form.html"

    list_display = (
        "id",
        "name",
        "language",
        "tags",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "language",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "id",
        "name",
        "tags",
    )
    readonly_fields = (
        "id",
        "video_mp4",
        "cartesia_voice_id",
        "created_at",
        "updated_at",
    )

    def save_model(self, request, obj, form, change):
        # Determine what actions to take
        should_normalize_video = not change or self._needs_video_renormalization(obj)
        should_cleanup_old_video = change and should_normalize_video

        # Clean up previous normalized video if replacing
        if should_cleanup_old_video:
            old_normalized_video = self._get_existing_normalized_video(obj)
            if old_normalized_video:
                old_normalized_video.delete(save=False)
                obj.video_mp4 = None

        super().save_model(request, obj, form, change)

        # Queue video normalization if needed
        if should_normalize_video and obj.video:
            convert_video_to_mp4.delay(obj.id)

        # Queue voice cloning if needed
        if not change or self._needs_voice_reclone(obj):
            create_voice_clone.delay(obj.id)

    def _needs_video_renormalization(self, obj):
        """Check if the source video has changed and needs re-normalization."""
        try:
            existing = Creator.objects.get(pk=obj.pk)
            return existing.video != obj.video
        except Creator.DoesNotExist:
            return bool(obj.video)

    def _get_existing_normalized_video(self, obj):
        """Retrieve the current normalized video file from storage."""
        try:
            return Creator.objects.get(pk=obj.pk).video_mp4
        except Creator.DoesNotExist:
            return None

    def _needs_voice_reclone(self, obj):
        """Check if the language or video has changed and needs voice re-cloning."""
        try:
            existing = Creator.objects.get(pk=obj.pk)
            return existing.video != obj.video or existing.language != obj.language
        except Creator.DoesNotExist:
            return bool(obj.video)
