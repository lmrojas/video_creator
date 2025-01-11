from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class VideoProject(models.Model):
    """Modelo para proyectos de video."""
    
    STATUS_CHOICES = [
        ('draft', _('Borrador')),
        ('processing', _('Procesando')),
        ('completed', _('Completado')),
        ('failed', _('Fallido')),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='video_projects',
        verbose_name=_('Usuario')
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name=_('Título')
    )
    
    description = models.TextField(
        verbose_name=_('Descripción')
    )
    
    template = models.ForeignKey(
        'VideoTemplate',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects',
        verbose_name=_('Template')
    )
    
    script = models.TextField(
        blank=True,
        verbose_name=_('Script')
    )
    
    base_media = models.FileField(
        upload_to='project_media/',
        null=True,
        blank=True,
        verbose_name=_('Medio Principal')
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name=_('Estado')
    )
    
    notification_email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_('Email para Notificaciones')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Fecha de Creación')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Última Actualización')
    )
    
    class Meta:
        verbose_name = _('Proyecto de Video')
        verbose_name_plural = _('Proyectos de Video')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title 