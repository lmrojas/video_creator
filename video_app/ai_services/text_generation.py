import openai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class TextGenerationService:
    """Servicio para generar texto usando GPT para scripts y descripciones."""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.default_model = "gpt-3.5-turbo"
    
    def generate_script(self, project_info, style=None, duration=None, max_tokens=1000):
        """
        Genera un script para el video basado en la información del proyecto.
        
        Args:
            project_info (dict): Información del proyecto (título, descripción, etc.)
            style (str, optional): Estilo deseado para el video
            duration (int, optional): Duración objetivo en segundos
            max_tokens (int): Máximo número de tokens a generar
            
        Returns:
            dict: Script generado y metadata
        """
        try:
            # Construir el prompt
            prompt = self._build_script_prompt(project_info, style, duration)
            
            # Generar el script
            response = openai.ChatCompletion.create(
                model=self.default_model,
                messages=[
                    {"role": "system", "content": "Eres un experto guionista de videos."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            # Extraer y formatear el script
            script = response.choices[0].message.content.strip()
            
            return {
                'script': script,
                'estimated_duration': self._estimate_duration(script),
                'scenes': self._extract_scenes(script)
            }
            
        except Exception as e:
            logger.error(f"Error generating script: {str(e)}")
            raise
    
    def generate_description(self, title, target_audience=None, keywords=None, max_tokens=200):
        """
        Genera una descripción atractiva para el video.
        
        Args:
            title (str): Título del video
            target_audience (str, optional): Audiencia objetivo
            keywords (list, optional): Palabras clave a incluir
            max_tokens (int): Máximo número de tokens a generar
            
        Returns:
            str: Descripción generada
        """
        try:
            # Construir el prompt
            prompt = self._build_description_prompt(title, target_audience, keywords)
            
            # Generar la descripción
            response = openai.ChatCompletion.create(
                model=self.default_model,
                messages=[
                    {"role": "system", "content": "Eres un experto en marketing digital y descripción de videos."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating description: {str(e)}")
            raise
    
    def _build_script_prompt(self, project_info, style=None, duration=None):
        """Construye el prompt para la generación del script."""
        prompt = f"Crea un script detallado para un video sobre: {project_info['title']}\n"
        prompt += f"Descripción del proyecto: {project_info.get('description', '')}\n"
        
        if style:
            prompt += f"Estilo deseado: {style}\n"
        
        if duration:
            prompt += f"Duración objetivo: {duration} segundos\n"
        
        prompt += "\nEl script debe incluir:\n"
        prompt += "1. Escenas claramente definidas\n"
        prompt += "2. Descripción visual de cada escena\n"
        prompt += "3. Texto o diálogo para cada escena\n"
        prompt += "4. Sugerencias de música o efectos de sonido\n"
        
        return prompt
    
    def _build_description_prompt(self, title, target_audience=None, keywords=None):
        """Construye el prompt para la generación de la descripción."""
        prompt = f"Crea una descripción atractiva y optimizada para SEO para un video titulado: {title}\n"
        
        if target_audience:
            prompt += f"Audiencia objetivo: {target_audience}\n"
        
        if keywords:
            prompt += f"Palabras clave a incluir: {', '.join(keywords)}\n"
        
        prompt += "\nLa descripción debe:\n"
        prompt += "1. Captar la atención en los primeros segundos\n"
        prompt += "2. Incluir un llamado a la acción\n"
        prompt += "3. Ser concisa pero informativa\n"
        prompt += "4. Usar las palabras clave de manera natural\n"
        
        return prompt
    
    def _estimate_duration(self, script):
        """Estima la duración del video basado en el script."""
        # Aproximación básica: 2.5 segundos por palabra
        words = len(script.split())
        return words * 2.5
    
    def _extract_scenes(self, script):
        """Extrae las escenas del script generado."""
        # Implementación básica - se puede mejorar con NLP
        scenes = []
        current_scene = ""
        
        for line in script.split('\n'):
            if line.strip().lower().startswith(('escena', 'scene')):
                if current_scene:
                    scenes.append(current_scene.strip())
                current_scene = line
            else:
                current_scene += f"\n{line}"
        
        if current_scene:
            scenes.append(current_scene.strip())
        
        return scenes 