from django.db import models
from django.utils.translation import gettext_lazy as _
from .video_project import VideoProject

class VideoProcessingTask(models.Model):
    """Modelo para gestionar las tareas de procesamiento de video."""
    
    STATUS_CHOICES = [
        ('pending', _('Pendiente')),
        ('processing', _('Procesando')),
        ('completed', _('Completado')),
        ('failed', _('Fallido')),
    ]

    project = models.ForeignKey(
        VideoProject,
        on_delete=models.CASCADE,
        related_name='processing_tasks'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    started_at = models.DateTimeField(
        null=True,
        blank=True
    )
    
    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )
    
    error_message = models.TextField(
        blank=True
    )
    
    progress = models.IntegerField(
        default=0,
        help_text=_('Progreso del procesamiento en porcentaje')
    )
    
    output_file = models.FileField(
        upload_to='processed_videos/',
        null=True,
        blank=True
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Tarea de Procesamiento')
        verbose_name_plural = _('Tareas de Procesamiento')

    def __str__(self):
        return f'Procesamiento de {self.project.title} - {self.get_status_display()}' 