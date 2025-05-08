from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, Schools, Campuses, Issues, StudentSubmissions

@admin.register(StudentSubmissions)
class StudentSubmissionsAdmin(admin.ModelAdmin):
    list_display = ("id", "student_ids", "school", "issue", "date", "show_face_image")
    readonly_fields = ("show_face_image",)

    def show_face_image(self, obj):
        if obj.face_image:
            return format_html('<img src="{}" style="width: 120px; height: auto; border-radius: 8px;" />', obj.face_image.url)
        return "(No image)"

    show_face_image.short_description = "Face Photo"

# Register other models
admin.site.register(Profile)
admin.site.register(Schools)
admin.site.register(Campuses)
admin.site.register(Issues)
