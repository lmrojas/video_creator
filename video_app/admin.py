from django.contrib import admin
from .models import VideoProject, VideoTemplate, VideoScene, VideoElement

@admin.register(VideoProject)
class VideoProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'updated_at']
    search_fields = ['title', 'description']

@admin.register(VideoTemplate)
class VideoTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'difficulty_level']
    list_filter = ['category', 'difficulty_level', 'industry']
    search_fields = ['name', 'description']

@admin.register(VideoScene)
class VideoSceneAdmin(admin.ModelAdmin):
    list_display = ['project', 'order', 'duration']
    list_filter = ['project']
    ordering = ['project', 'order']

@admin.register(VideoElement)
class VideoElementAdmin(admin.ModelAdmin):
    list_display = ['scene', 'element_type', 'start_time']
    list_filter = ['element_type', 'scene__project']
    search_fields = ['content']
