from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from ..models import VideoProject
from ..forms.project import VideoProjectForm
from django.views.generic import View
from django.http import JsonResponse
from ..models import VideoScene, AudioElement
from ..forms.project import TTSGenerationForm
from ..ai_services.tts import TTSService
import json

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

class GenerateAudioView(LoginRequiredMixin, View):
    """Vista para generar audio usando TTS."""
    
    def post(self, request, scene_id):
        scene = get_object_or_404(VideoScene, id=scene_id, project__user=request.user)
        form = TTSGenerationForm(request.POST)
        
        if form.is_valid():
            try:
                # Crear el elemento de audio sin guardar
                audio_element = form.save(commit=False)
                audio_element.scene = scene
                audio_element.audio_type = 'tts'
                
                # Generar el audio
                tts_service = TTSService()
                output_filename = f"tts_{scene.id}_{hash(form.cleaned_data['text_content'])}.wav"
                
                audio_path = tts_service.generate_audio(
                    text=form.cleaned_data['text_content'],
                    voice_id=form.cleaned_data['voice_id'],
                    output_filename=output_filename
                )
                
                # Guardar la ruta del archivo generado
                audio_element.content = audio_path
                audio_element.save()
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Audio generado correctamente',
                    'audio_element': {
                        'id': audio_element.id,
                        'content_url': audio_element.content.url if audio_element.content else None,
                        'start_time': audio_element.start_time,
                        'end_time': audio_element.end_time,
                        'volume': audio_element.volume
                    }
                })
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Error al generar el audio: {str(e)}'
                }, status=500)
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Formulario inválido',
                'errors': form.errors
            }, status=400) 