from django.db import models
from django.utils.translation import gettext_lazy as _

TEMPLATE_CATEGORIES = [
    ('educational', _('Educativo')),
    ('marketing', _('Marketing')),
    ('social', _('Redes Sociales')),
    ('business', _('Negocios')),
    ('personal', _('Personal')),
]

DIFFICULTY_LEVELS = [
    ('beginner', _('Principiante')),
    ('intermediate', _('Intermedio')),
    ('advanced', _('Avanzado')),
]

class VideoTemplate(models.Model):
    """Modelo para las plantillas de video."""
    
    name = models.CharField(
        max_length=100,
        verbose_name=_('Nombre')
    )
    
    description = models.TextField(
        verbose_name=_('Descripción')
    )
    
    category = models.CharField(
        max_length=20,
        choices=TEMPLATE_CATEGORIES,
        verbose_name=_('Categoría')
    )
    
    difficulty_level = models.CharField(
        max_length=20,
        choices=DIFFICULTY_LEVELS,
        verbose_name=_('Nivel de Dificultad')
    )
    
    preview_image = models.ImageField(
        upload_to='template_previews/',
        null=True,
        blank=True,
        verbose_name=_('Imagen de Vista Previa')
    )
    
    configuration = models.JSONField(
        default=dict,
        verbose_name=_('Configuración')
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
        verbose_name = _('Template de Video')
        verbose_name_plural = _('Templates de Video')
        ordering = ['name']
    
    def __str__(self):
        return self.name 