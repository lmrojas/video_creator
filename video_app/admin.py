from django.contrib import admin
from .models import VideoProject, VideoTemplate, VideoProcessingTask

@admin.register(VideoProject)
class VideoProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    date_hierarchy = 'created_at'

@admin.register(VideoTemplate)
class VideoTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'difficulty_level')
    list_filter = ('category', 'difficulty_level')
    search_fields = ('name', 'description')

@admin.register(VideoProcessingTask)
class VideoProcessingTaskAdmin(admin.ModelAdmin):
    list_display = ('project', 'status', 'progress', 'started_at', 'completed_at')
    list_filter = ('status', 'created_at')
    search_fields = ('project__title', 'error_message')
    date_hierarchy = 'created_at'
