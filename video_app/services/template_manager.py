from typing import Dict, List
import json
from django.conf import settings
import os
from django.core.cache import cache
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from ..models import VideoTemplate

class TemplateManager:
    """
    Gestor de plantillas de video que maneja la creación y gestión de plantillas predefinidas.
    """
    
    TEMPLATE_CATEGORIES = [
        ('educational', _('Educativo')),
        ('marketing', _('Marketing')),
        ('social', _('Redes Sociales')),
        ('business', _('Negocios')),
        ('personal', _('Personal')),
    ]
    
    DEFAULT_TRANSITIONS = {
        'fade': {
            'duration': 1.0,
            'type': 'fade',
            'params': {}
        },
        'slide_left': {
            'duration': 1.0,
            'type': 'slide',
            'params': {'direction': 'left'}
        },
        'slide_right': {
            'duration': 1.0,
            'type': 'slide',
            'params': {'direction': 'right'}
        },
        'zoom_in': {
            'duration': 1.0,
            'type': 'zoom',
            'params': {'scale': 1.5}
        }
    }
    
    DEFAULT_EFFECTS = {
        'blur': {
            'type': 'blur',
            'params': {'radius': 5}
        },
        'brightness': {
            'type': 'brightness',
            'params': {'factor': 1.2}
        },
        'contrast': {
            'type': 'contrast',
            'params': {'factor': 1.2}
        },
        'grayscale': {
            'type': 'grayscale',
            'params': {}
        },
        'fade_in': {
            'type': 'fade_in',
            'params': {'duration': 1.0}
        }
    }

    def __init__(self):
        self.cache_key_prefix = 'template_manager'
    
    def get_all_templates(self):
        """Obtener todas las plantillas."""
        cache_key = f"{self.cache_key_prefix}_all_templates"
        templates = cache.get(cache_key)
        
        if templates is None:
            templates = VideoTemplate.objects.all()
            cache.set(cache_key, templates, timeout=3600)  # Cache por 1 hora
        
        return templates
    
    def get_template_by_id(self, template_id):
        """Obtener una plantilla por su ID."""
        cache_key = f"{self.cache_key_prefix}_template_{template_id}"
        template = cache.get(cache_key)
        
        if template is None:
            template = VideoTemplate.objects.get(id=template_id)
            cache.set(cache_key, template, timeout=3600)
        
        return template
    
    def filter_templates(self, category=None, difficulty_level=None, search_query=None):
        """Filtrar plantillas por categoría, nivel de dificultad y búsqueda."""
        templates = VideoTemplate.objects.all()
        
        if category:
            templates = templates.filter(category=category)
        
        if difficulty_level:
            templates = templates.filter(difficulty_level=difficulty_level)
        
        if search_query:
            templates = templates.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        return templates
    
    def get_template_preview(self, template_id):
        """Obtener la vista previa de una plantilla."""
        template = self.get_template_by_id(template_id)
        return template.preview_image.url if template.preview_image else None
    
    def get_template_configuration(self, template_id):
        """Obtener la configuración de una plantilla."""
        template = self.get_template_by_id(template_id)
        return template.configuration

    @classmethod
    def create_promotional_template(cls) -> Dict:
        """Crea una plantilla promocional básica."""
        return {
            'name': 'Promoción Básica',
            'description': 'Plantilla para videos promocionales cortos',
            'category': 'PROMO',
            'difficulty_level': 1,
            'industry': 'TECH',
            'estimated_duration': 30,
            'json_structure': {
                'scenes': [
                    {
                        'duration': 5.0,
                        'transition': cls.DEFAULT_TRANSITIONS['fade'],
                        'elements': [
                            {
                                'type': 'text',
                                'content': 'Título Principal',
                                'position': {'x': 0.5, 'y': 0.3},
                                'size': {'width': 0.8, 'height': 0.2},
                                'effects': [cls.DEFAULT_EFFECTS['fade_in']]
                            },
                            {
                                'type': 'video',
                                'content': 'background.mp4',
                                'position': {'x': 0, 'y': 0},
                                'size': {'width': 1.0, 'height': 1.0},
                                'effects': [cls.DEFAULT_EFFECTS['blur']]
                            }
                        ]
                    },
                    {
                        'duration': 10.0,
                        'transition': cls.DEFAULT_TRANSITIONS['slide_left'],
                        'elements': [
                            {
                                'type': 'text',
                                'content': 'Descripción del Producto',
                                'position': {'x': 0.5, 'y': 0.5},
                                'size': {'width': 0.6, 'height': 0.3},
                                'effects': []
                            }
                        ]
                    }
                ]
            }
        }

    @classmethod
    def create_educational_template(cls) -> Dict:
        """Crea una plantilla educativa básica."""
        return {
            'name': 'Tutorial Básico',
            'description': 'Plantilla para videos educativos y tutoriales',
            'category': 'EDUC',
            'difficulty_level': 1,
            'industry': 'TECH',
            'estimated_duration': 300,
            'json_structure': {
                'scenes': [
                    {
                        'duration': 10.0,
                        'transition': cls.DEFAULT_TRANSITIONS['fade'],
                        'elements': [
                            {
                                'type': 'text',
                                'content': 'Introducción al Tema',
                                'position': {'x': 0.5, 'y': 0.2},
                                'size': {'width': 0.8, 'height': 0.1},
                                'effects': [cls.DEFAULT_EFFECTS['fade_in']]
                            }
                        ]
                    },
                    {
                        'duration': 240.0,
                        'transition': None,
                        'elements': [
                            {
                                'type': 'video',
                                'content': 'screen_recording.mp4',
                                'position': {'x': 0, 'y': 0},
                                'size': {'width': 1.0, 'height': 0.8},
                                'effects': []
                            },
                            {
                                'type': 'text',
                                'content': 'Explicación Paso a Paso',
                                'position': {'x': 0.5, 'y': 0.9},
                                'size': {'width': 0.8, 'height': 0.1},
                                'effects': []
                            }
                        ]
                    }
                ]
            }
        }

    @classmethod
    def initialize_default_templates(cls):
        """Inicializa las plantillas predefinidas en la base de datos."""
        templates = [
            cls.create_promotional_template(),
            cls.create_educational_template()
        ]
        
        for template_data in templates:
            VideoTemplate.objects.get_or_create(
                name=template_data['name'],
                defaults=template_data
            )

    @classmethod
    def apply_effect(cls, element_data: Dict, effect_name: str, params: Dict = None) -> Dict:
        """Aplica un efecto a un elemento."""
        if effect_name in cls.DEFAULT_EFFECTS:
            effect = cls.DEFAULT_EFFECTS[effect_name].copy()
            if params:
                effect['params'].update(params)
            if 'effects' not in element_data:
                element_data['effects'] = []
            element_data['effects'].append(effect)
        return element_data

    @classmethod
    def apply_transition(cls, scene_data: Dict, transition_name: str, params: Dict = None) -> Dict:
        """Aplica una transición a una escena."""
        if transition_name in cls.DEFAULT_TRANSITIONS:
            transition = cls.DEFAULT_TRANSITIONS[transition_name].copy()
            if params:
                transition['params'].update(params)
            scene_data['transition'] = transition
        return scene_data 