from TTS.api import TTS
import os
from django.conf import settings
import torch

class TTSService:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # Inicializamos TTS con un modelo multilingüe
        self.tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)
        
    def generate_audio(self, text, language='es', output_path=None):
        """
        Genera audio a partir de texto
        """
        try:
            if output_path is None:
                output_path = os.path.join(settings.MEDIA_ROOT, 'generated_audio', 'temp.wav')
                
            # Aseguramos que el directorio existe
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Generamos el audio
            self.tts.tts_to_file(
                text=text,
                file_path=output_path,
                language=language,
                speaker_wav=None  # Se puede añadir un archivo de voz de referencia
            )
            
            return output_path
        except Exception as e:
            print(f"Error en la generación de audio: {str(e)}")
            return None
            
    def generate_voice_clone(self, text, reference_audio_path, output_path=None):
        """
        Genera audio clonando una voz de referencia
        """
        try:
            if output_path is None:
                output_path = os.path.join(settings.MEDIA_ROOT, 'generated_audio', 'cloned.wav')
                
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Generamos el audio con la voz clonada
            self.tts.tts_to_file(
                text=text,
                file_path=output_path,
                speaker_wav=reference_audio_path
            )
            
            return output_path
        except Exception as e:
            print(f"Error en la clonación de voz: {str(e)}")
            return None
            
    def generate_multiple_voices(self, script_parts, language='es'):
        """
        Genera audio para múltiples partes de un script con diferentes voces
        """
        audio_files = []
        try:
            for i, (speaker, text) in enumerate(script_parts):
                output_path = os.path.join(
                    settings.MEDIA_ROOT, 
                    'generated_audio', 
                    f'part_{i}.wav'
                )
                
                # Podemos variar parámetros para cada voz
                self.tts.tts_to_file(
                    text=text,
                    file_path=output_path,
                    language=language,
                    speaker_wav=None
                )
                
                audio_files.append(output_path)
                
            return audio_files
        except Exception as e:
            print(f"Error en la generación de múltiples voces: {str(e)}")
            return None 