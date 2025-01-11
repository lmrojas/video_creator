from moviepy.editor import VideoFileClip, ImageClip, TextClip, CompositeVideoClip
from moviepy.video.fx.all import *
import numpy as np

class VideoEffectsService:
    """
    Servicio para aplicar efectos a clips de video.
    """

    @staticmethod
    def apply_blur(clip, radius=5):
        """Aplica un efecto de desenfoque al clip."""
        return clip.fx(vfx.blur, radius)

    @staticmethod
    def apply_brightness(clip, factor=1.2):
        """Ajusta el brillo del clip."""
        return clip.fx(vfx.colorx, factor)

    @staticmethod
    def apply_contrast(clip, factor=1.2):
        """Ajusta el contraste del clip."""
        def modify_contrast(image):
            mean = image.mean()
            return np.clip((image - mean) * factor + mean, 0, 255).astype('uint8')
        return clip.fl_image(modify_contrast)

    @staticmethod
    def apply_grayscale(clip):
        """Convierte el clip a escala de grises."""
        return clip.fx(vfx.blackwhite)

    @staticmethod
    def apply_fade_in(clip, duration=1.0):
        """Aplica un efecto de aparición gradual."""
        return clip.fx(vfx.fadein, duration)

    @staticmethod
    def apply_fade_out(clip, duration=1.0):
        """Aplica un efecto de desaparición gradual."""
        return clip.fx(vfx.fadeout, duration)

    @staticmethod
    def apply_slide(clip, direction='left', duration=1.0):
        """Aplica un efecto de deslizamiento."""
        w, h = clip.size
        if direction == 'left':
            def slide(t):
                return ('center', h/2 + int(w*(t/duration - 1)))
        elif direction == 'right':
            def slide(t):
                return ('center', h/2 + int(-w*(t/duration - 1)))
        else:
            return clip
        
        return clip.set_position(slide)

    @staticmethod
    def apply_zoom(clip, scale=1.5, duration=1.0):
        """Aplica un efecto de zoom."""
        def zoom(t):
            if t < duration:
                return 1 + (scale - 1) * t/duration
            return scale
        return clip.fx(vfx.resize, zoom)

    @classmethod
    def apply_effects(cls, clip, effects_list):
        """
        Aplica una lista de efectos a un clip.
        
        Args:
            clip: El clip de video/imagen al que aplicar los efectos
            effects_list: Lista de diccionarios con efectos y sus parámetros
        
        Returns:
            Clip con los efectos aplicados
        """
        for effect in effects_list:
            effect_type = effect.get('type')
            params = effect.get('params', {})
            
            if effect_type == 'blur':
                clip = cls.apply_blur(clip, **params)
            elif effect_type == 'brightness':
                clip = cls.apply_brightness(clip, **params)
            elif effect_type == 'contrast':
                clip = cls.apply_contrast(clip, **params)
            elif effect_type == 'grayscale':
                clip = cls.apply_grayscale(clip)
            elif effect_type == 'fade_in':
                clip = cls.apply_fade_in(clip, **params)
            elif effect_type == 'fade_out':
                clip = cls.apply_fade_out(clip, **params)
            elif effect_type == 'slide':
                clip = cls.apply_slide(clip, **params)
            elif effect_type == 'zoom':
                clip = cls.apply_zoom(clip, **params)
        
        return clip

    @classmethod
    def apply_transition(cls, clip1, clip2, transition_data):
        """
        Aplica una transición entre dos clips.
        
        Args:
            clip1: Primer clip
            clip2: Segundo clip
            transition_data: Diccionario con tipo de transición y parámetros
        
        Returns:
            Clip con la transición aplicada
        """
        transition_type = transition_data.get('type')
        duration = transition_data.get('duration', 1.0)
        params = transition_data.get('params', {})
        
        if transition_type == 'fade':
            clip1 = clip1.fx(vfx.fadeout, duration)
            clip2 = clip2.fx(vfx.fadein, duration)
        elif transition_type == 'slide':
            direction = params.get('direction', 'left')
            clip2 = cls.apply_slide(clip2, direction, duration)
        elif transition_type == 'zoom':
            scale = params.get('scale', 1.5)
            clip2 = cls.apply_zoom(clip2, scale, duration)
        
        return CompositeVideoClip([clip1, clip2.set_start(clip1.duration - duration)]) 