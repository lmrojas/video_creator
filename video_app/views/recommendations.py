from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import VideoProject
from ..ai_services.recommendations import RecommendationService
import logging

logger = logging.getLogger(__name__)

class GetRecommendationsView(LoginRequiredMixin, View):
    """Vista para obtener recomendaciones de templates y estilos."""
    
    def get(self, request, project_id):
        try:
            # Obtener el proyecto
            project = VideoProject.objects.get(
                id=project_id,
                user=request.user
            )
            
            # Inicializar el servicio de recomendaciones
            recommendation_service = RecommendationService()
            
            # Obtener historial de proyectos del usuario
            user_history = VideoProject.objects.filter(
                user=request.user
            ).exclude(id=project_id)
            
            # Obtener recomendaciones de templates
            recommended_templates = recommendation_service.recommend_templates(
                project_description=f"{project.title} {project.description}",
                user_history=user_history
            )
            
            # Obtener recomendaciones de estilo
            style_recommendations = recommendation_service.recommend_style(project)
            
            # Preparar respuesta
            response_data = {
                'status': 'success',
                'recommended_templates': [
                    {
                        'id': template.id,
                        'name': template.name,
                        'description': template.description,
                        'category': template.get_category_display(),
                        'difficulty_level': template.get_difficulty_level_display(),
                        'preview_url': template.preview_image.url if template.preview_image else None
                    }
                    for template in recommended_templates
                ],
                'style_recommendations': style_recommendations
            }
            
            return JsonResponse(response_data)
            
        except VideoProject.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Proyecto no encontrado'
            }, status=404)
            
        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'Error al obtener recomendaciones'
            }, status=500) 