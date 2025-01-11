import os
from pathlib import Path
import pyttsx3
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class TTSService:
    """Servicio de Text-to-Speech para generar audio a partir de texto."""
    
    def __init__(self):
        self.output_path = os.path.join(settings.MEDIA_ROOT, 'audio_elements')
        Path(self.output_path).mkdir(parents=True, exist_ok=True)
        self.engine = pyttsx3.init()
        self.available_voices = self._get_available_voices()
        self._init_engine()
    
    def _init_engine(self):
        """Inicializa el motor TTS con configuración por defecto."""
        try:
            self.engine.setProperty('rate', 150)    # Velocidad de habla
            self.engine.setProperty('volume', 1.0)  # Volumen (0.0 a 1.0)
            
            # Establecer voz por defecto en español si está disponible
            spanish_voice = next(
                (v for v in self.available_voices if 'spanish' in v['name'].lower()),
                None
            )
            if spanish_voice:
                self.engine.setProperty('voice', spanish_voice['id'])
        except Exception as e:
            logger.error(f"Error initializing TTS engine: {str(e)}")
    
    def _get_available_voices(self):
        """Obtiene la lista de voces disponibles."""
        try:
            voices = []
            for voice in self.engine.getProperty('voices'):
                voices.append({
                    'id': voice.id,
                    'name': voice.name,
                    'languages': voice.languages,
                    'gender': voice.gender
                })
            return voices
        except Exception as e:
            logger.error(f"Error getting available voices: {str(e)}")
            return []
    
    def change_voice(self, voice_id):
        """Cambia la voz del motor TTS."""
        try:
            self.engine.setProperty('voice', voice_id)
            return True
        except Exception as e:
            logger.error(f"Error changing voice to {voice_id}: {str(e)}")
            return False
    
    def generate_audio(self, text, voice_id=None, output_filename=None):
        """
        Genera un archivo de audio a partir de texto.
        
        Args:
            text (str): Texto a convertir en audio
            voice_id (str, optional): ID de la voz a utilizar
            output_filename (str, optional): Nombre del archivo de salida
            
        Returns:
            str: Ruta al archivo de audio generado
        """
        try:
            if voice_id:
                self.change_voice(voice_id)
            
            if not output_filename:
                output_filename = f"tts_{hash(text)}.wav"
            
            output_path = os.path.join(self.output_path, output_filename)
            
            # Generar el audio
            self.engine.save_to_file(text, output_path)
            self.engine.runAndWait()
            
            return output_path
        except Exception as e:
            logger.error(f"Error generating audio: {str(e)}")
            raise
    
    def get_available_voices(self):
        """Retorna la lista de voces disponibles."""
        return self.available_voices 