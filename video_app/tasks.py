from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .services.video_processor import VideoProcessor
from .models import VideoProject

@shared_task
def process_video_project(project_id):
    """
    Tarea de Celery para procesar un proyecto de video de forma asíncrona.
    Envía actualizaciones de progreso a través de WebSocket.
    """
    channel_layer = get_channel_layer()
    group_name = f"video_processing_{project_id}"

    try:
        # Obtener el proyecto
        project = VideoProject.objects.get(id=project_id)
        
        # Notificar inicio del procesamiento
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "processing_update",
                "message": "Iniciando procesamiento",
                "progress": 0
            }
        )

        # Crear instancia del procesador
        processor = VideoProcessor(project_id)
        
        # Notificar progreso
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "processing_update",
                "message": "Procesando escenas",
                "progress": 50
            }
        )

        # Procesar el proyecto
        output_path = processor.process_project()
        
        if output_path:
            # Actualizar el proyecto con la ruta del video procesado
            project.output_video = output_path.replace(settings.MEDIA_ROOT + '/', '')
            project.status = 'completed'
            project.save()

            # Notificar éxito
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    "type": "processing_update",
                    "message": "Procesamiento completado",
                    "progress": 100,
                    "output_url": project.output_video.url
                }
            )
        else:
            raise Exception("Error al procesar el video")

    except Exception as e:
        # Actualizar estado del proyecto
        if 'project' in locals():
            project.status = 'failed'
            project.error_message = str(e)
            project.save()

        # Notificar error
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "processing_update",
                "message": f"Error: {str(e)}",
                "progress": -1
            }
        )
        
        # Re-lanzar la excepción para que Celery la maneje
        raise 