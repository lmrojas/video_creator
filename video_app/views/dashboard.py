from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from ..models import VideoProject

class DashboardView(LoginRequiredMixin, TemplateView):
    """Vista principal del dashboard."""
    template_name = 'video_app/dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_projects'] = VideoProject.objects.filter(
            user=self.request.user
        ).order_by('-created_at')[:5]
        return context

class ProjectListView(LoginRequiredMixin, ListView):
    """Vista de lista de proyectos."""
    model = VideoProject
    template_name = 'video_app/dashboard/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10
    
    def get_queryset(self):
        return VideoProject.objects.filter(
            user=self.request.user
        ).order_by('-created_at')

class ProjectDetailView(LoginRequiredMixin, DetailView):
    """Vista de detalle de proyecto."""
    model = VideoProject
    template_name = 'video_app/dashboard/project_detail.html'
    context_object_name = 'project'
    
    def get_object(self):
        return get_object_or_404(
            VideoProject,
            id=self.kwargs['pk'],
            user=self.request.user
        ) 