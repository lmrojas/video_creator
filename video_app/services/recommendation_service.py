from django.db.models import Count, Q
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from ..models import VideoProject, VideoTemplate

class RecommendationService:
    """Servicio para recomendaciones de plantillas y contenido"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
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
            usage_count=Count('videoproject')
        ).order_by('-usage_count')[:limit]
        
    def _get_similar_templates(self, user_projects, limit=5):
        """Encuentra plantillas similares basadas en los proyectos del usuario"""
        # Obtener todas las plantillas
        all_templates = VideoTemplate.objects.all()
        
        if not all_templates.exists():
            return []
            
        # Crear matriz TF-IDF de descripciones
        descriptions = [template.description for template in all_templates]
        tfidf_matrix = self.vectorizer.fit_transform(descriptions)
        
        # Obtener descripción combinada de proyectos del usuario
        user_description = " ".join([p.description for p in user_projects if p.description])
        user_vector = self.vectorizer.transform([user_description])
        
        # Calcular similitud
        similarities = cosine_similarity(user_vector, tfidf_matrix)[0]
        
        # Obtener índices de las plantillas más similares
        similar_indices = similarities.argsort()[-limit:][::-1]
        
        # Devolver las plantillas correspondientes
        template_list = list(all_templates)
        return [template_list[i] for i in similar_indices]
        
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
            'suggestions': self._get_script_suggestions({'script': script})
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
            
        # TODO: Implementar análisis real de contenido multimedia
        return {
            'status': 'success',
            'has_media': True,
            'suggestions': self._get_media_suggestions(project)
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
            
        # TODO: Implementar análisis real de calidad de media
        suggestions.extend([
            "Asegúrate de que el video tiene buena iluminación",
            "Verifica la calidad del audio",
            "Considera añadir transiciones entre escenas"
        ])
        
        return suggestions 