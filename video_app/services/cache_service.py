from django.core.cache import cache
from django.conf import settings
import hashlib
import json

class CacheService:
    """Servicio para gestionar el caché de la aplicación"""
    
    # Tiempos de expiración por tipo de contenido (en segundos)
    EXPIRATION_TIMES = {
        'template': 3600,  # 1 hora
        'project': 1800,   # 30 minutos
        'analytics': 300,  # 5 minutos
        'preview': 7200    # 2 horas
    }
    
    @staticmethod
    def generate_key(prefix, *args):
        """
        Genera una clave única para el caché.
        
        Args:
            prefix: Prefijo para identificar el tipo de contenido
            *args: Argumentos adicionales para generar la clave
            
        Returns:
            str: Clave única para el caché
        """
        # Convertir todos los argumentos a string y unirlos
        key_parts = [str(arg) for arg in args]
        key_string = '_'.join(key_parts)
        
        # Generar hash MD5 de la cadena
        hash_object = hashlib.md5(key_string.encode())
        hash_string = hash_object.hexdigest()
        
        # Retornar clave con prefijo
        return f"video_app_{prefix}_{hash_string}"
    
    @classmethod
    def get_or_set(cls, prefix, callback, *args, **kwargs):
        """
        Obtiene un valor del caché o lo genera si no existe.
        
        Args:
            prefix: Prefijo para la clave
            callback: Función para generar el valor si no está en caché
            *args: Argumentos para generar la clave
            **kwargs: Argumentos adicionales para el callback
            
        Returns:
            El valor almacenado en caché o generado por el callback
        """
        key = cls.generate_key(prefix, *args)
        value = cache.get(key)
        
        if value is None:
            value = callback(**kwargs)
            expiration = cls.EXPIRATION_TIMES.get(prefix, 3600)
            cache.set(key, value, expiration)
        
        return value
    
    @classmethod
    def invalidate(cls, prefix, *args):
        """
        Invalida una entrada específica del caché.
        
        Args:
            prefix: Prefijo de la clave
            *args: Argumentos para generar la clave
        """
        key = cls.generate_key(prefix, *args)
        cache.delete(key)
    
    @classmethod
    def invalidate_pattern(cls, prefix):
        """
        Invalida todas las entradas que coincidan con un prefijo.
        
        Args:
            prefix: Prefijo para invalidar
        """
        if hasattr(cache, 'delete_pattern'):
            cache.delete_pattern(f"video_app_{prefix}_*")
    
    @classmethod
    def cache_template(cls, template_id, data):
        """
        Almacena en caché los datos de un template.
        
        Args:
            template_id: ID del template
            data: Datos a almacenar
        """
        key = cls.generate_key('template', template_id)
        cache.set(key, data, cls.EXPIRATION_TIMES['template'])
    
    @classmethod
    def cache_project_preview(cls, project_id, frame_data):
        """
        Almacena en caché los datos de preview de un proyecto.
        
        Args:
            project_id: ID del proyecto
            frame_data: Datos del frame a almacenar
        """
        key = cls.generate_key('preview', project_id)
        cache.set(key, frame_data, cls.EXPIRATION_TIMES['preview'])
    
    @classmethod
    def get_project_preview(cls, project_id):
        """
        Obtiene los datos de preview de un proyecto.
        
        Args:
            project_id: ID del proyecto
            
        Returns:
            dict: Datos del preview o None si no está en caché
        """
        key = cls.generate_key('preview', project_id)
        return cache.get(key)