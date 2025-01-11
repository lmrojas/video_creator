from django.db.models import Count
from ..models import VideoProject, VideoTemplate

class RecommendationService:
    """Servicio para recomendaciones de plantillas y contenido"""
    
    def get_template_recommendations(self, user_id, limit=5):
        """Obtiene recomendaciones de plantillas para un usuario"""
        # Obtener proyectos del usuario
        user_projects = VideoProject.objects.filter(user_id=user_id)
        
        if not user_projects.exists():
            # Si no hay proyectos, recomendar las plantillas más populares
            return self._get_popular_templates(limit)
            
        # Obtener plantillas similares basadas en los proyectos del usuario
        similar_templates = self._get_similar_templates(user_projects, limit)
        return similar_templates
        
    def get_content_recommendations(self, project_id):
        """Proporciona recomendaciones de contenido para un proyecto"""
        try:
            project = VideoProject.objects.get(id=project_id)
            
            recommendations = {
                'script': self._analyze_script(project.script),
                'media': self._analyze_media(project)
            }
            return recommendations
        except VideoProject.DoesNotExist:
            return None
            
    def get_improvement_suggestions(self, project_id):
        """Genera sugerencias para mejorar un proyecto"""
        try:
            project = VideoProject.objects.get(id=project_id)
            
            suggestions = {
                'script': self._get_script_suggestions(project),
                'media': self._get_media_suggestions(project)
            }
            return suggestions
        except VideoProject.DoesNotExist:
            return None
            
    def _get_popular_templates(self, limit=5):
        """Obtiene las plantillas más populares"""
        return VideoTemplate.objects.annotate(
            usage_count=Count('projects')
        ).order_by('-usage_count')[:limit]
        
    def _get_similar_templates(self, user_projects, limit=5):
        """Encuentra plantillas similares basadas en los proyectos del usuario"""
        # Obtener categorías más usadas por el usuario
        user_categories = set(
            user_projects.exclude(template__isnull=True)
            .values_list('template__category', flat=True)
        )
        
        if not user_categories:
            return self._get_popular_templates(limit)
        
        # Obtener plantillas de categorías similares
        return VideoTemplate.objects.filter(
            category__in=user_categories
        ).order_by('?')[:limit]
        
    def _analyze_script(self, script):
        """Analiza el script y genera recomendaciones"""
        if not script:
            return {
                'status': 'warning',
                'message': 'No hay script para analizar',
                'suggestions': ['Añade un script para obtener recomendaciones']
            }
            
        recommendations = {
            'status': 'success',
            'length': len(script),
            'suggestions': []
        }
        return recommendations
        
    def _analyze_media(self, project):
        """Analiza el contenido multimedia y genera recomendaciones"""
        if not project.base_media:
            return {
                'status': 'warning',
                'message': 'No hay contenido multimedia para analizar',
                'suggestions': ['Añade contenido multimedia para obtener recomendaciones']
            }
            
        return {
            'status': 'success',
            'has_media': True,
            'suggestions': []
        }
        
    def _get_script_suggestions(self, project):
        """Genera sugerencias para mejorar el script"""
        suggestions = []
        
        if not project.script:
            suggestions.append("Añade un script para mejorar la calidad del video")
            return suggestions
            
        script = project.script.lower()
        
        # Análisis básico del script
        if len(script) < 100:
            suggestions.append("El script es muy corto, considera expandirlo")
        if len(script.split()) < 20:
            suggestions.append("Añade más detalles al script")
        if '.' not in script:
            suggestions.append("Usa puntuación adecuada en el script")
            
        return suggestions
        
    def _get_media_suggestions(self, project):
        """Genera sugerencias para mejorar el contenido multimedia"""
        suggestions = []
        
        if not project.base_media:
            suggestions.append("Añade contenido multimedia al proyecto")
            return suggestions
            
        suggestions.extend([
            "Asegúrate de que el video tiene buena iluminación",
            "Verifica la calidad del audio",
            "Considera añadir transiciones entre escenas"
        ])
        
        return suggestions 