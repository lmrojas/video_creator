from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from ..models import VideoProject, VideoScene

class SceneEditorView(LoginRequiredMixin, TemplateView):
    """Vista para el editor de escenas."""
    template_name = 'video_app/editor/scene_editor.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener el proyecto y la escena
        project_id = self.kwargs.get('project_id')
        scene_id = self.kwargs.get('scene_id')
        
        project = get_object_or_404(
            VideoProject,
            id=project_id,
            user=self.request.user
        )
        
        scene = None
        if scene_id:
            scene = get_object_or_404(
                VideoScene,
                id=scene_id,
                project=project
            )
        
        context.update({
            'project': project,
            'scene': scene,
            'scenes': project.scenes.all().order_by('order')
        })
        
        return context 