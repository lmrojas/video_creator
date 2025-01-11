from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import VideoProject, VideoProcessingTask
from .services.video_processing import VideoProcessingService

@shared_task
def process_video_project(project_id):
    """Tarea asíncrona para procesar un proyecto de video."""
    try:
        project = VideoProject.objects.get(id=project_id)
        
        # Crear tarea de procesamiento
        processing_task = VideoProcessingTask.objects.create(
            project=project,
            status='pending'
        )
        
        # Iniciar el procesamiento
        service = VideoProcessingService(processing_task)
        service.process()
        
        # Enviar notificación por email si se proporcionó
        if project.notification_email:
            send_mail(
                subject='Tu video está listo',
                message=f'Tu video "{project.title}" ha sido procesado exitosamente.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[project.notification_email],
                fail_silently=True
            )
            
        return True
        
    except Exception as e:
        if project.notification_email:
            send_mail(
                subject='Error en el procesamiento de tu video',
                message=f'Hubo un error al procesar tu video "{project.title}": {str(e)}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[project.notification_email],
                fail_silently=True
            )
        return False 