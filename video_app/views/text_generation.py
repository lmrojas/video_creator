from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import VideoProject
from ..ai_services.text_generation import TextGenerationService
import logging

logger = logging.getLogger(__name__)

class GenerateScriptView(LoginRequiredMixin, View):
    """Vista para generar scripts de video."""
    
    def post(self, request, project_id):
        try:
            # Obtener el proyecto
            project = VideoProject.objects.get(
                id=project_id,
                user=request.user
            )
            
            # Obtener parámetros de la solicitud
            style = request.POST.get('style')
            duration = request.POST.get('duration')
            if duration:
                duration = int(duration)
            
            # Preparar información del proyecto
            project_info = {
                'title': project.title,
                'description': project.description
            }
            
            # Inicializar el servicio y generar el script
            text_service = TextGenerationService()
            result = text_service.generate_script(
                project_info=project_info,
                style=style,
                duration=duration
            )
            
            # Actualizar el script del proyecto
            project.script = result['script']
            project.save(update_fields=['script'])
            
            return JsonResponse({
                'status': 'success',
                'script': result['script'],
                'estimated_duration': result['estimated_duration'],
                'scenes': result['scenes']
            })
            
        except VideoProject.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Proyecto no encontrado'
            }, status=404)
            
        except Exception as e:
            logger.error(f"Error generating script: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

class GenerateDescriptionView(LoginRequiredMixin, View):
    """Vista para generar descripciones de video."""
    
    def post(self, request, project_id):
        try:
            # Obtener el proyecto
            project = VideoProject.objects.get(
                id=project_id,
                user=request.user
            )
            
            # Obtener parámetros de la solicitud
            target_audience = request.POST.get('target_audience')
            keywords = request.POST.getlist('keywords[]', None)
            
            # Inicializar el servicio y generar la descripción
            text_service = TextGenerationService()
            description = text_service.generate_description(
                title=project.title,
                target_audience=target_audience,
                keywords=keywords
            )
            
            # Actualizar la descripción del proyecto
            project.description = description
            project.save(update_fields=['description'])
            
            return JsonResponse({
                'status': 'success',
                'description': description
            })
            
        except VideoProject.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Proyecto no encontrado'
            }, status=404)
            
        except Exception as e:
            logger.error(f"Error generating description: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500) 