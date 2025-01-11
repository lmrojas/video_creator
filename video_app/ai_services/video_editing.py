from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx import resize, speedx
import os
from django.conf import settings

class VideoEditingService:
    def __init__(self):
        self.output_dir = os.path.join(settings.MEDIA_ROOT, 'generated_videos')
        os.makedirs(self.output_dir, exist_ok=True)

    def create_video(self, template, content, output_filename=None):
        """
        Crea un video basado en una plantilla y contenido
        """
        try:
            if output_filename is None:
                output_filename = 'output.mp4'
                
            output_path = os.path.join(self.output_dir, output_filename)
            
            # Cargamos el video base si existe
            if content.get('base_video'):
                base = VideoFileClip(content['base_video'])
            else:
                # Crear un video desde cero con el contenido proporcionado
                pass
            
            # Procesamos cada elemento según la plantilla
            clips = []
            for element in template['elements']:
                if element['type'] == 'text':
                    clip = self._create_text_clip(element, content)
                elif element['type'] == 'video':
                    clip = self._create_video_clip(element, content)
                elif element['type'] == 'audio':
                    clip = self._create_audio_clip(element, content)
                
                if clip:
                    clips.append(clip)
            
            # Componemos el video final
            final_video = CompositeVideoClip(clips)
            
            # Aplicamos efectos globales si existen
            if template.get('effects'):
                final_video = self._apply_effects(final_video, template['effects'])
            
            # Guardamos el video
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                fps=30
            )
            
            return output_path
            
        except Exception as e:
            print(f"Error en la creación del video: {str(e)}")
            return None

    def _create_text_clip(self, element, content):
        """
        Crea un clip de texto con los parámetros especificados
        """
        try:
            text = content.get(element['content_key'], element.get('default_text', ''))
            
            text_clip = TextClip(
                text,
                fontsize=element.get('fontsize', 30),
                color=element.get('color', 'white'),
                font=element.get('font', 'Arial')
            )
            
            # Aplicamos posición y duración
            text_clip = text_clip.set_position(element.get('position', 'center'))
            text_clip = text_clip.set_duration(element.get('duration', 5))
            
            # Aplicamos efectos si existen
            if element.get('effects'):
                text_clip = self._apply_effects(text_clip, element['effects'])
                
            return text_clip
            
        except Exception as e:
            print(f"Error creando clip de texto: {str(e)}")
            return None

    def _create_video_clip(self, element, content):
        """
        Crea un clip de video con los parámetros especificados
        """
        try:
            video_path = content.get(element['content_key'])
            if not video_path:
                return None
                
            video_clip = VideoFileClip(video_path)
            
            # Aplicamos transformaciones básicas
            if element.get('resize'):
                video_clip = video_clip.resize(element['resize'])
            
            if element.get('position'):
                video_clip = video_clip.set_position(element['position'])
                
            if element.get('duration'):
                video_clip = video_clip.set_duration(element['duration'])
                
            # Aplicamos efectos si existen
            if element.get('effects'):
                video_clip = self._apply_effects(video_clip, element['effects'])
                
            return video_clip
            
        except Exception as e:
            print(f"Error creando clip de video: {str(e)}")
            return None

    def _create_audio_clip(self, element, content):
        """
        Crea un clip de audio con los parámetros especificados
        """
        try:
            audio_path = content.get(element['content_key'])
            if not audio_path:
                return None
                
            audio_clip = AudioFileClip(audio_path)
            
            if element.get('duration'):
                audio_clip = audio_clip.set_duration(element['duration'])
                
            # Aplicamos efectos si existen
            if element.get('effects'):
                audio_clip = self._apply_effects(audio_clip, element['effects'])
                
            return audio_clip
            
        except Exception as e:
            print(f"Error creando clip de audio: {str(e)}")
            return None

    def _apply_effects(self, clip, effects):
        """
        Aplica una lista de efectos a un clip
        """
        try:
            for effect in effects:
                if effect['type'] == 'fade_in':
                    clip = clip.fadein(effect.get('duration', 1))
                elif effect['type'] == 'fade_out':
                    clip = clip.fadeout(effect.get('duration', 1))
                elif effect['type'] == 'speed':
                    clip = speedx(clip, effect.get('factor', 1.5))
                # Añadir más efectos según sea necesario
                
            return clip
            
        except Exception as e:
            print(f"Error aplicando efectos: {str(e)}")
            return clip 