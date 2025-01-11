import magic
from django.core.exceptions import ValidationError
from django.conf import settings
import os

class ContentValidator:
    """Servicio para validar contenido multimedia"""
    
    # Tipos MIME permitidos por categoría
    ALLOWED_TYPES = {
        'image': [
            'image/jpeg',
            'image/png',
            'image/gif'
        ],
        'video': [
            'video/mp4',
            'video/quicktime',
            'video/x-msvideo'
        ],
        'audio': [
            'audio/mpeg',
            'audio/wav',
            'audio/x-wav'
        ]
    }
    
    # Límites de tamaño por tipo (en bytes)
    SIZE_LIMITS = {
        'image': 10 * 1024 * 1024,  # 10MB
        'video': 100 * 1024 * 1024, # 100MB
        'audio': 50 * 1024 * 1024   # 50MB
    }
    
    def validate_file(self, file, expected_type=None):
        """
        Valida un archivo multimedia.
        
        Args:
            file: Archivo a validar
            expected_type: Tipo esperado ('image', 'video', 'audio')
            
        Raises:
            ValidationError: Si el archivo no cumple con los requisitos
        """
        if not file:
            raise ValidationError('No se proporcionó ningún archivo')
        
        # Validar tamaño
        if file.size > self.SIZE_LIMITS.get(expected_type, 100 * 1024 * 1024):
            raise ValidationError(
                f'El archivo excede el tamaño máximo permitido de '
                f'{self.SIZE_LIMITS[expected_type] / (1024 * 1024)}MB'
            )
        
        # Validar tipo MIME
        mime = magic.from_buffer(file.read(1024), mime=True)
        file.seek(0)  # Resetear el puntero del archivo
        
        if expected_type and mime not in self.ALLOWED_TYPES.get(expected_type, []):
            raise ValidationError(
                f'Tipo de archivo no permitido. Se esperaba {expected_type}, '
                f'pero se recibió {mime}'
            )
        
        # Validar contenido malicioso
        self._scan_for_malware(file)
    
    def _scan_for_malware(self, file):
        """
        Escanea un archivo en busca de malware.
        En una implementación real, aquí se integraría un servicio de antivirus.
        """
        # Implementación básica de ejemplo
        suspicious_extensions = ['.exe', '.bat', '.sh', '.php']
        if any(file.name.lower().endswith(ext) for ext in suspicious_extensions):
            raise ValidationError('El archivo podría ser malicioso')
    
    def validate_script(self, script):
        """
        Valida el contenido de un script.
        
        Args:
            script: Texto del script a validar
            
        Raises:
            ValidationError: Si el script no cumple con los requisitos
        """
        if not script or not script.strip():
            raise ValidationError('El script no puede estar vacío')
        
        # Validar longitud mínima
        if len(script.split()) < 10:
            raise ValidationError('El script debe tener al menos 10 palabras')
        
        # Validar contenido inapropiado
        self._check_inappropriate_content(script)
    
    def _check_inappropriate_content(self, text):
        """
        Verifica si el texto contiene contenido inapropiado.
        En una implementación real, aquí se integraría un servicio de moderación.
        """
        # Lista básica de palabras prohibidas
        banned_words = ['spam', 'scam', 'hack']
        
        # Convertir a minúsculas para comparación
        text_lower = text.lower()
        
        # Buscar palabras prohibidas
        found_words = [word for word in banned_words if word in text_lower]
        
        if found_words:
            raise ValidationError(
                'El texto contiene contenido inapropiado: ' + 
                ', '.join(found_words)
            ) 