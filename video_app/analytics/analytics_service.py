from datetime import datetime, timedelta
from django.db.models import Count
from django.utils import timezone
from ..models import VideoProject

class AnalyticsService:
    """Servicio para recolectar y analizar métricas de proyectos"""
    
    def get_user_analytics(self, user_id):
        """Obtener analíticas del usuario"""
        now = timezone.now()
        start_date = now - timedelta(days=30)
        
        # Obtener proyectos del usuario
        projects = VideoProject.objects.filter(user_id=user_id)
        
        # Proyectos por estado
        total_projects = projects.count()
        completed_projects = projects.filter(status='completed').count()
        in_progress = projects.filter(status='processing').count()
        
        # Proyectos este mes
        this_month = projects.filter(created_at__gte=start_date).count()
        
        # Proyectos por día (últimos 30 días)
        projects_by_day = {}
        for i in range(30):
            date = now - timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            count = projects.filter(
                created_at__date=date.date()
            ).count()
            projects_by_day[date_str] = count
        
        return {
            'total_projects': total_projects,
            'completed_projects': completed_projects,
            'in_progress': in_progress,
            'this_month': this_month,
            'projects_by_day': projects_by_day
        }
    
    def collect_project_metrics(self, project_id):
        """Recolectar métricas de un proyecto específico"""
        project = VideoProject.objects.get(id=project_id)
        
        # Métricas básicas
        processing_time = 0
        if project.status == 'completed':
            processing_time = (project.updated_at - project.created_at).total_seconds()
        
        # Estadísticas de media
        script_length = len(project.script.split()) if project.script else 0
        
        # Interacciones del usuario
        user_interactions = {
            'edits': 0,  # TODO: Implementar tracking de ediciones
            'previews': 0  # TODO: Implementar tracking de previsualizaciones
        }
        
        return {
            'processing_time': processing_time,
            'media_stats': {
                'script_length': script_length
            },
            'user_interactions': user_interactions
        } 