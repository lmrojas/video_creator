import os
from datetime import datetime
from django.conf import settings
from django.core.files import File
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips
from ..models import VideoProcessingTask

class VideoProcessingService:
    """Servicio para procesar videos."""
    
    def __init__(self, processing_task):
        self.task = processing_task
        self.project = processing_task.project
        self.output_path = os.path.join(settings.MEDIA_ROOT, 'processed_videos')
        os.makedirs(self.output_path, exist_ok=True)
    
    def process(self):
        """Procesa el video según la configuración del proyecto."""
        try:
            self.task.status = 'processing'
            self.task.started_at = datetime.now()
            self.task.save()
            
            # Procesar el video base o crear uno desde la imagen
            if self.project.base_media:
                if self._is_video(self.project.base_media.path):
                    base_clip = VideoFileClip(self.project.base_media.path)
                else:
                    base_clip = ImageClip(self.project.base_media.path)
            
            # Aplicar efectos según el template
            processed_clip = self._apply_template_effects(base_clip)
            
            # Generar el archivo de salida
            output_filename = f'processed_{self.project.id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.mp4'
            output_path = os.path.join(self.output_path, output_filename)
            
            processed_clip.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True
            )
            
            # Guardar el resultado
            with open(output_path, 'rb') as output_file:
                self.task.output_file.save(output_filename, File(output_file))
            
            self.task.status = 'completed'
            self.task.completed_at = datetime.now()
            self.task.progress = 100
            self.task.save()
            
            # Limpiar
            processed_clip.close()
            if 'base_clip' in locals():
                base_clip.close()
            
            if os.path.exists(output_path):
                os.remove(output_path)
                
        except Exception as e:
            self.task.status = 'failed'
            self.task.error_message = str(e)
            self.task.save()
            raise
    
    def _is_video(self, file_path):
        """Determina si un archivo es un video."""
        video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv']
        return any(file_path.lower().endswith(ext) for ext in video_extensions)
    
    def _apply_template_effects(self, clip):
        """Aplica los efectos del template al clip."""
        # Aquí implementaremos los efectos específicos del template
        # Por ahora, solo devolvemos el clip original
        return clip
    
    def update_progress(self, progress):
        """Actualiza el progreso del procesamiento."""
        self.task.progress = progress
        self.task.save(update_fields=['progress']) 