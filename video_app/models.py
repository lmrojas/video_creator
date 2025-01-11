# Sistema de creación y edición de videos con IA
# Modelos principales para la gestión de proyectos y templates de video

from django.db import models
from django.contrib.auth.models import User

# Constantes para las opciones de categorías de templates
TEMPLATE_CATEGORIES = [
    ('PROMO', 'Promocional'),  # Videos promocionales y marketing
    ('EDUC', 'Educativo'),     # Contenido educativo y tutoriales
    ('CORP', 'Corporativo')    # Videos corporativos y presentaciones
]

# Niveles de dificultad para los templates
DIFFICULTY_LEVELS = [
    (1, 'Básico'),      # Templates simples con pocas secciones
    (2, 'Intermedio'),  # Templates con efectos y transiciones moderadas
    (3, 'Avanzado')     # Templates complejos con efectos avanzados
]

# Industrias objetivo para los templates
INDUSTRIES = [
    ('TECH', 'Tecnología'),  # Sector tecnológico y software
    ('RETL', 'Retail'),      # Comercio minorista y ventas
    ('HLTH', 'Salud')        # Sector salud y bienestar
]

# Estados posibles de un proyecto de video
PROJECT_STATUS = [
    ('draft', 'Borrador'),      # Proyecto en edición
    ('processing', 'Procesando'),# Video en proceso de generación
    ('completed', 'Completado'), # Video generado exitosamente
    ('failed', 'Fallido')       # Error en la generación
]

class VideoProject(models.Model):
    """
    Modelo principal para proyectos de video.
    Gestiona toda la información relacionada con un proyecto de video específico.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    script = models.TextField(blank=True)
    base_media = models.FileField(upload_to='user_uploads/', blank=True, null=True)
    template = models.ForeignKey('VideoTemplate', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Campos para seguimiento del estado del proyecto
    status = models.CharField(
        max_length=20,
        choices=PROJECT_STATUS,
        default='draft'
    )
    progress = models.IntegerField(default=0)  # Progreso de 0 a 100
    error_message = models.TextField(blank=True)
    output_video = models.FileField(
        upload_to='generated_videos/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.title} (de {self.user.username})"

    class Meta:
        ordering = ['-created_at']  # Ordenar por fecha de creación descendente

    @property
    def get_status_class(self):
        """Retorna la clase de Bootstrap correspondiente al estado."""
        status_classes = {
            'draft': 'secondary',
            'processing': 'warning',
            'completed': 'success',
            'failed': 'danger'
        }
        return status_classes.get(self.status, 'secondary')

    @property
    def is_editable(self):
        """Indica si el proyecto puede ser editado."""
        return self.status in ['draft', 'failed']

    @property
    def can_be_processed(self):
        """Indica si el proyecto puede ser procesado."""
        return (
            self.status in ['draft', 'failed'] and
            bool(self.script.strip()) and
            (bool(self.base_media) or bool(self.template))
        )

    @property
    def duration(self):
        """Retorna la duración total del video en segundos."""
        return sum(scene.duration for scene in self.scenes.all())

    def start_processing(self):
        """Inicia el procesamiento del video."""
        if self.can_be_processed:
            self.status = 'processing'
            self.progress = 0
            self.error_message = ''
            self.save()
            return True
        return False

    def complete_processing(self, output_path=None):
        """Marca el procesamiento como completado."""
        self.status = 'completed'
        self.progress = 100
        if output_path:
            from django.core.files import File
            with open(output_path, 'rb') as f:
                self.output_video.save(
                    f'video_{self.pk}.mp4',
                    File(f),
                    save=False
                )
        self.save()

    def fail_processing(self, error_message):
        """Marca el procesamiento como fallido."""
        self.status = 'failed'
        self.error_message = error_message
        self.save()

    def update_progress(self, progress):
        """Actualiza el progreso del procesamiento."""
        self.progress = min(max(progress, 0), 100)
        self.save(update_fields=['progress'])

class VideoTemplate(models.Model):
    """
    Modelo para templates de video.
    Define la estructura y características de los templates disponibles.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    preview_image = models.ImageField(upload_to='templates/previews/', blank=True, null=True)
    json_structure = models.JSONField()  # Estructura del template en formato JSON
    category = models.CharField(max_length=50, choices=TEMPLATE_CATEGORIES)
    difficulty_level = models.IntegerField(choices=DIFFICULTY_LEVELS)
    industry = models.CharField(max_length=50, choices=INDUSTRIES)
    estimated_duration = models.IntegerField(help_text="Duración en segundos")

    class Meta:
        indexes = [
            models.Index(fields=['category', 'difficulty_level']),  # Índice para búsquedas frecuentes
            models.Index(fields=['industry'])
        ]

    def __str__(self):
        return self.name

class VideoScene(models.Model):
    """
    Modelo para representar una escena individual dentro de un proyecto de video.
    Cada escena puede contener múltiples elementos (texto, imágenes, videos, etc.).
    """
    project = models.ForeignKey('VideoProject', on_delete=models.CASCADE, related_name='scenes')
    order = models.IntegerField()
    duration = models.FloatField(help_text="Duration in seconds")
    transition_type = models.CharField(max_length=50, default='none')
    transition_duration = models.FloatField(default=0.0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Escena {self.order} de {self.project.title}"

class VideoElement(models.Model):
    """
    Modelo para representar elementos individuales dentro de una escena.
    Puede ser texto, imagen, video, forma, etc.
    """
    ELEMENT_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('effect', 'Effect'),
    ]

    scene = models.ForeignKey(VideoScene, on_delete=models.CASCADE, related_name='elements')
    element_type = models.CharField(max_length=20, choices=ELEMENT_TYPES)
    content = models.TextField()  # Para texto o rutas de archivos
    position_x = models.FloatField(default=0.0)
    position_y = models.FloatField(default=0.0)
    width = models.FloatField(default=1.0)
    height = models.FloatField(default=1.0)
    start_time = models.FloatField(default=0.0)
    end_time = models.FloatField(null=True, blank=True)
    effects = models.JSONField(default=dict)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.get_element_type_display()} en {self.scene}"

    @property
    def position(self):
        """Retorna la posición como un diccionario."""
        return {"x": self.position_x, "y": self.position_y}

    @property
    def size(self):
        """Retorna el tamaño como un diccionario."""
        return {"width": self.width, "height": self.height}

class AudioElement(models.Model):
    AUDIO_TYPES = [
        ('tts', 'Text to Speech'),
        ('upload', 'Uploaded Audio'),
        ('music', 'Background Music'),
    ]
    
    scene = models.ForeignKey('VideoScene', on_delete=models.CASCADE, related_name='audio_elements')
    audio_type = models.CharField(max_length=10, choices=AUDIO_TYPES)
    content = models.FileField(upload_to='audio_elements/', null=True, blank=True)
    text_content = models.TextField(null=True, blank=True)
    voice_id = models.CharField(max_length=100, null=True, blank=True)
    start_time = models.FloatField(default=0.0)
    end_time = models.FloatField(null=True, blank=True)
    volume = models.FloatField(default=1.0)
    
    class Meta:
        ordering = ['start_time']
    
    def __str__(self):
        return f"{self.get_audio_type_display()} - {self.scene.project.title}"
