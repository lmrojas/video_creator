from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ImageClip
from moviepy.video.fx.all import resize
import os
from django.conf import settings
from ..models import VideoProject, VideoScene, VideoElement
from .effects_service import VideoEffectsService
from .template_manager import TemplateManager

class VideoProcessor:
    def __init__(self, project_id):
        self.project = VideoProject.objects.get(id=project_id)
        self.output_path = os.path.join(settings.MEDIA_ROOT, 'processed_videos')
        os.makedirs(self.output_path, exist_ok=True)
        self.effects_service = VideoEffectsService()

    def process_scene(self, scene):
        """
        Procesa una escena completa con sus elementos y efectos.
        """
        clips = []
        
        # Procesar cada elemento en la escena
        for element in scene.elements.all().order_by('start_time'):
            if element.element_type == 'text':
                clip = self._process_text_element(element)
            elif element.element_type == 'image':
                clip = self._process_image_element(element)
            elif element.element_type == 'video':
                clip = self._process_video_element(element)
            
            if clip:
                # Aplicar efectos si existen
                if element.effects:
                    clip = self.effects_service.apply_effects(clip, element.effects)
                clips.append(clip)
        
        # Crear la composición final de la escena
        if clips:
            scene_clip = CompositeVideoClip(clips, size=(1920, 1080))
            
            # Aplicar transición si existe
            if scene.transition_type != 'none':
                transition_data = {
                    'type': scene.transition_type,
                    'duration': scene.transition_duration
                }
                scene_clip = self.effects_service.apply_transition(
                    scene_clip,
                    scene_clip,  # En este caso el mismo clip, pero podría ser otro
                    transition_data
                )
            
            return scene_clip
        return None

    def _process_text_element(self, element):
        """
        Procesa un elemento de texto con sus propiedades y efectos.
        """
        try:
            text_clip = TextClip(
                element.content,
                fontsize=48,
                color='white',
                size=(element.width * 1920, element.height * 1080)
            )
            
            # Posicionar el texto
            text_clip = text_clip.set_position((
                element.position_x * 1920,
                element.position_y * 1080
            ))
            
            # Aplicar duración
            if element.end_time:
                text_clip = text_clip.set_duration(element.end_time - element.start_time)
            
            return text_clip
        except Exception as e:
            print(f"Error processing text element: {str(e)}")
            return None

    def _process_image_element(self, element):
        """
        Procesa un elemento de imagen con sus propiedades y efectos.
        """
        try:
            image_path = os.path.join(settings.MEDIA_ROOT, element.content)
            if not os.path.exists(image_path):
                return None
            
            image_clip = ImageClip(image_path)
            
            # Redimensionar y posicionar
            image_clip = image_clip.resize(
                width=element.width * 1920,
                height=element.height * 1080
            ).set_position((
                element.position_x * 1920,
                element.position_y * 1080
            ))
            
            # Aplicar duración
            if element.end_time:
                image_clip = image_clip.set_duration(element.end_time - element.start_time)
            
            return image_clip
        except Exception as e:
            print(f"Error processing image element: {str(e)}")
            return None

    def _process_video_element(self, element):
        """
        Procesa un elemento de video con sus propiedades y efectos.
        """
        try:
            video_path = os.path.join(settings.MEDIA_ROOT, element.content)
            if not os.path.exists(video_path):
                return None
            
            video_clip = VideoFileClip(video_path)
            
            # Redimensionar y posicionar
            video_clip = video_clip.resize(
                width=element.width * 1920,
                height=element.height * 1080
            ).set_position((
                element.position_x * 1920,
                element.position_y * 1080
            ))
            
            # Aplicar duración
            if element.end_time:
                video_clip = video_clip.subclip(
                    element.start_time,
                    element.end_time
                )
            
            return video_clip
        except Exception as e:
            print(f"Error processing video element: {str(e)}")
            return None

    def process_project(self):
        """
        Procesa el proyecto completo, aplicando la plantilla si existe.
        """
        try:
            # Obtener todas las escenas ordenadas
            scenes = self.project.scenes.all().order_by('order')
            final_clips = []
            
            # Procesar cada escena
            for scene in scenes:
                scene_clip = self.process_scene(scene)
                if scene_clip:
                    final_clips.append(scene_clip)
            
            # Si no hay clips, retornar None
            if not final_clips:
                return None
            
            # Concatenar todas las escenas
            final_video = CompositeVideoClip(final_clips)
            
            # Generar el nombre del archivo de salida
            output_filename = f"project_{self.project.id}_final.mp4"
            output_path = os.path.join(self.output_path, output_filename)
            
            # Renderizar el video final
            final_video.write_videofile(
                output_path,
                fps=30,
                codec='libx264',
                audio_codec='aac'
            )
            
            return output_path
        except Exception as e:
            print(f"Error processing project: {str(e)}")
            return None

    def apply_template(self, template_id):
        """
        Aplica una plantilla al proyecto actual.
        """
        try:
            template = VideoTemplate.objects.get(id=template_id)
            structure = template.json_structure
            
            # Limpiar escenas existentes
            self.project.scenes.all().delete()
            
            # Crear nuevas escenas desde la plantilla
            for i, scene_data in enumerate(structure['scenes']):
                scene = VideoScene.objects.create(
                    project=self.project,
                    order=i,
                    duration=scene_data['duration'],
                    transition_type=scene_data.get('transition', {}).get('type', 'none'),
                    transition_duration=scene_data.get('transition', {}).get('duration', 0.0)
                )
                
                # Crear elementos para la escena
                for element_data in scene_data['elements']:
                    VideoElement.objects.create(
                        scene=scene,
                        element_type=element_data['type'],
                        content=element_data['content'],
                        position_x=element_data['position']['x'],
                        position_y=element_data['position']['y'],
                        width=element_data['size']['width'],
                        height=element_data['size']['height'],
                        effects=element_data.get('effects', [])
                    )
            
            return True
        except Exception as e:
            print(f"Error applying template: {str(e)}")
            return False 