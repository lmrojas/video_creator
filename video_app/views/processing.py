from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ..models import VideoProject, VideoProcessingTask

class ProcessingMonitorView(LoginRequiredMixin, DetailView):
    """Vista para monitorear el progreso del procesamiento de video."""
    
    model = VideoProject
    template_name = 'video_app/processing/monitor.html'
    context_object_name = 'project'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['processing_task'] = self.object.processing_tasks.last()
        return context

def get_processing_status(request, pk):
    """Vista para obtener el estado actual del procesamiento vía AJAX."""
    if not request.is_ajax():
        return JsonResponse({'error': 'Solo se permiten solicitudes AJAX'}, status=400)
    
    project = get_object_or_404(VideoProject, pk=pk, user=request.user)
    task = project.processing_tasks.last()
    
    if not task:
        return JsonResponse({
            'status': 'not_found',
            'message': 'No se encontró una tarea de procesamiento'
        })
    
    return JsonResponse({
        'status': task.status,
        'progress': task.progress,
        'started_at': task.started_at.isoformat() if task.started_at else None,
        'completed_at': task.completed_at.isoformat() if task.completed_at else None,
        'error_message': task.error_message if task.error_message else None,
        'output_url': task.output_file.url if task.output_file else None
    }) 