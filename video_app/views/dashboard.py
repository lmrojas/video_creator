from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import VideoProject
from ..analytics.analytics_service import AnalyticsService
from ..services.recommendation_service import RecommendationService

class DashboardView(LoginRequiredMixin, TemplateView):
    """Vista principal del dashboard que muestra estadísticas y proyectos recientes"""
    template_name = 'video_app/dashboard/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        analytics_service = AnalyticsService()
        recommendation_service = RecommendationService()
        
        context['user_analytics'] = analytics_service.get_user_analytics(self.request.user)
        context['recent_projects'] = VideoProject.objects.filter(
            user=self.request.user
        ).order_by('-updated_at')[:5]
        context['recommendations'] = recommendation_service.get_recommendations(self.request.user)
        return context

class ProjectListView(LoginRequiredMixin, ListView):
    """Vista que muestra la lista de proyectos del usuario"""
    model = VideoProject
    template_name = 'video_app/dashboard/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = VideoProject.objects.filter(user=self.request.user)
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        return queryset.order_by('-updated_at')

class ProjectDetailView(LoginRequiredMixin, DetailView):
    """Vista que muestra los detalles de un proyecto específico"""
    model = VideoProject
    template_name = 'video_app/dashboard/project_detail.html'
    context_object_name = 'project'
    
    def get_queryset(self):
        return VideoProject.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        analytics_service = AnalyticsService()
        context['project_metrics'] = analytics_service.get_project_metrics(self.object)
        return context 