from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View

from ..models import VideoProject
from ..forms.project import VideoProjectForm

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    """Vista para actualizar un proyecto."""
    model = VideoProject
    form_class = VideoProjectForm
    template_name = 'video_app/project/edit.html'
    
    def get_object(self):
        return get_object_or_404(
            VideoProject,
            id=self.kwargs['pk'],
            user=self.request.user
        )
    
    def get_success_url(self):
        return reverse_lazy('video_app:project_detail', kwargs={'pk': self.object.pk})

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    """Vista para eliminar un proyecto."""
    model = VideoProject
    template_name = 'video_app/project/delete.html'
    success_url = reverse_lazy('video_app:project_list')
    
    def get_object(self):
        return get_object_or_404(
            VideoProject,
            id=self.kwargs['pk'],
            user=self.request.user
        ) 