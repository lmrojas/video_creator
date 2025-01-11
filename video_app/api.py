from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import VideoProject
from .tasks import process_video_project

class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return VideoProject.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def generate(self, request, pk=None):
        """
        Inicia el proceso de generación de video
        """
        project = self.get_object()
        
        # Verificar si el proyecto ya está en proceso
        if project.status == 'processing':
            return Response(
                {'error': 'El proyecto ya está siendo procesado'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Actualizar estado y lanzar tarea
        project.status = 'processing'
        project.progress = 0
        project.error_message = ''
        project.save()
        
        # Lanzar tarea asíncrona
        process_video_project.delay(project.id)
        
        return Response({'status': 'Generación iniciada'}) 