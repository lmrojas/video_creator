import os
import magic
import cv2
import numpy as np
from PIL import Image
from django.core.exceptions import ValidationError
from django.conf import settings

class ContentValidator:
    """Servicio para validación de contenido multimedia"""
    
    # Tipos MIME permitidos
    ALLOWED_VIDEO_TYPES = ['video/mp4', 'video/mpeg', 'video/quicktime']
    ALLOWED_AUDIO_TYPES = ['audio/mpeg', 'audio/wav', 'audio/x-wav']
    ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif']
    
    # Límites de tamaño (en bytes)
    MAX_VIDEO_SIZE = 500 * 1024 * 1024  # 500MB
    MAX_AUDIO_SIZE = 50 * 1024 * 1024   # 50MB
    MAX_IMAGE_SIZE = 10 * 1024 * 1024   # 10MB
    
    def validate_file(self, file, file_type):
        """Valida un archivo según su tipo"""
        if not file:
            raise ValidationError("No se proporcionó ningún archivo")
            
        # Validar tamaño
        self._validate_file_size(file, file_type)
        
        # Validar tipo MIME
        mime_type = magic.from_buffer(file.read(1024), mime=True)
        file.seek(0)  # Resetear el puntero del archivo
        
        self._validate_mime_type(mime_type, file_type)
        
        # Validaciones específicas por tipo
        if file_type == 'video':
            self._validate_video_content(file)
        elif file_type == 'audio':
            self._validate_audio_content(file)
        elif file_type == 'image':
            self._validate_image_content(file)
            
    def _validate_file_size(self, file, file_type):
        """Valida el tamaño del archivo"""
        if file_type == 'video' and file.size > self.MAX_VIDEO_SIZE:
            raise ValidationError(f"El video excede el tamaño máximo permitido de {self.MAX_VIDEO_SIZE/1024/1024}MB")
        elif file_type == 'audio' and file.size > self.MAX_AUDIO_SIZE:
            raise ValidationError(f"El audio excede el tamaño máximo permitido de {self.MAX_AUDIO_SIZE/1024/1024}MB")
        elif file_type == 'image' and file.size > self.MAX_IMAGE_SIZE:
            raise ValidationError(f"La imagen excede el tamaño máximo permitido de {self.MAX_IMAGE_SIZE/1024/1024}MB")
            
    def _validate_mime_type(self, mime_type, file_type):
        """Valida el tipo MIME del archivo"""
        if file_type == 'video' and mime_type not in self.ALLOWED_VIDEO_TYPES:
            raise ValidationError(f"Tipo de video no permitido. Use: {', '.join(self.ALLOWED_VIDEO_TYPES)}")
        elif file_type == 'audio' and mime_type not in self.ALLOWED_AUDIO_TYPES:
            raise ValidationError(f"Tipo de audio no permitido. Use: {', '.join(self.ALLOWED_AUDIO_TYPES)}")
        elif file_type == 'image' and mime_type not in self.ALLOWED_IMAGE_TYPES:
            raise ValidationError(f"Tipo de imagen no permitido. Use: {', '.join(self.ALLOWED_IMAGE_TYPES)}")
            
    def _validate_video_content(self, file):
        """Validaciones específicas para videos"""
        temp_path = os.path.join(settings.MEDIA_ROOT, 'temp', file.name)
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
        
        with open(temp_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
                
        try:
            cap = cv2.VideoCapture(temp_path)
            if not cap.isOpened():
                raise ValidationError("El archivo de video está corrupto o no se puede leer")
            
            # Verificar duración y dimensiones
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count/fps
            
            if duration > 3600:  # Más de 1 hora
                raise ValidationError("El video excede la duración máxima permitida de 1 hora")
                
            cap.release()
        finally:
            os.remove(temp_path)
            
    def _validate_image_content(self, file):
        """Validaciones específicas para imágenes"""
        try:
            with Image.open(file) as img:
                # Verificar dimensiones
                if img.size[0] > 4096 or img.size[1] > 4096:
                    raise ValidationError("La imagen excede las dimensiones máximas permitidas de 4096x4096")
                    
                # Verificar que la imagen no está corrupta
                img.verify()
        except Exception as e:
            raise ValidationError(f"La imagen está corrupta o no es válida: {str(e)}")
            
    def _validate_audio_content(self, file):
        """Validaciones específicas para audio"""
        # TODO: Implementar validaciones específicas para audio
        pass 