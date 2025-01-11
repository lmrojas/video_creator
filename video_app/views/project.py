from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from ..models import VideoProject
from ..forms.project import VideoProjectForm

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    """Vista para editar un proyecto existente"""
    model = VideoProject
    form_class = VideoProjectForm
    template_name = 'video_app/project/edit.html'
    
    def get_queryset(self):
        return VideoProject.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('video_app:project_detail', kwargs={'pk': self.object.pk})

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    """Vista para eliminar un proyecto"""
    model = VideoProject
    template_name = 'video_app/project/delete.html'
    success_url = reverse_lazy('video_app:project_list')
    
    def get_queryset(self):
        return VideoProject.objects.filter(user=self.request.user)
    
    def get_object(self, queryset=None):
        """Asegura que solo el propietario pueda eliminar el proyecto"""
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionError("No tienes permiso para eliminar este proyecto")
        return obj 