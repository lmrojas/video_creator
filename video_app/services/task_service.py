import asyncio
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from ..ai_services.video_processor import VideoProcessor
from ..ai_services.video_analyzer import VideoAnalyzer
from ..models import VideoProject

class TaskService:
    def __init__(self):
        self.channel_layer = get_channel_layer()
        self.video_processor = VideoProcessor()
        self.video_analyzer = VideoAnalyzer()
        
    def process_video_async(self, project_id):
        """
        Inicia el procesamiento asíncrono de un video
        """
        try:
            # Obtener proyecto
            project = VideoProject.objects.get(id=project_id)
            
            # Iniciar tarea asíncrona
            asyncio.create_task(self._process_video_task(project))
            
            return {
                'status': 'started',
                'message': 'Procesamiento iniciado correctamente'
            }
            
        except VideoProject.DoesNotExist:
            return {
                'status': 'error',
                'message': 'Proyecto no encontrado'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    async def _process_video_task(self, project):
        """
        Tarea asíncrona para procesar un video
        """
        try:
            # Notificar inicio
            await self._send_status_update(project.id, 'processing', 'Iniciando procesamiento')
            
            # Procesar video
            result = self.video_processor.process_video(project.id)
            
            if result['status'] == 'success':
                # Analizar video procesado
                analysis = self.video_analyzer.analyze_video(result['output_path'])
                
                # Actualizar proyecto con resultados
                project.output_path = result['output_path']
                project.analysis_results = json.dumps(analysis)
                project.save()
                
                # Notificar éxito
                await self._send_status_update(project.id, 'completed', 'Procesamiento completado')
                
            else:
                # Notificar error
                await self._send_status_update(project.id, 'error', result['message'])
                
        except Exception as e:
            # Notificar error
            await self._send_status_update(project.id, 'error', str(e))
    
    async def _send_status_update(self, project_id, status, message):
        """
        Envía actualizaciones de estado a través de WebSocket
        """
        await self.channel_layer.group_send(
            f"project_{project_id}",
            {
                'type': 'status_update',
                'data': {
                    'status': status,
                    'message': message,
                    'timestamp': str(datetime.datetime.now())
                }
            }
        )
    
    def cancel_processing(self, project_id):
        """
        Cancela el procesamiento de un video
        """
        try:
            project = VideoProject.objects.get(id=project_id)
            
            # TODO: Implementar cancelación de tarea
            
            async_to_sync(self._send_status_update)(
                project_id,
                'cancelled',
                'Procesamiento cancelado'
            )
            
            return {
                'status': 'success',
                'message': 'Procesamiento cancelado correctamente'
            }
            
        except VideoProject.DoesNotExist:
            return {
                'status': 'error',
                'message': 'Proyecto no encontrado'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def get_processing_status(self, project_id):
        """
        Obtiene el estado actual del procesamiento
        """
        try:
            project = VideoProject.objects.get(id=project_id)
            
            # TODO: Implementar obtención de estado real
            
            return {
                'status': 'processing',
                'progress': 0,
                'message': 'En proceso'
            }
            
        except VideoProject.DoesNotExist:
            return {
                'status': 'error',
                'message': 'Proyecto no encontrado'
            } 