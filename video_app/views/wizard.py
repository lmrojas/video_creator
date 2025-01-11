# Sistema de creación de videos - Módulo de Wizard
# Implementa un asistente paso a paso para la creación de videos

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse

from ..models import VideoProject, VideoTemplate
from ..forms.wizard import (
    ProjectBasicInfoForm,
    TemplateSelectionForm,
    ScriptGenerationForm,
    MediaUploadForm,
    ProjectConfirmationForm
)
from ..services.text_generation import TextGenerationService
from ..tasks import process_video_project

class VideoWizardView(LoginRequiredMixin, TemplateView):
    """Vista base para el wizard de creación de videos."""
    
    template_name = 'video_app/wizard/base.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.request.session.get('wizard_project_id')
        
        if project_id:
            context['project'] = get_object_or_404(VideoProject, id=project_id)
        
        context['current_step'] = self.get_current_step()
        context['total_steps'] = 5
        return context
    
    def get_current_step(self):
        """Obtener el paso actual del wizard."""
        return 1

class ProjectBasicInfoView(VideoWizardView):
    """Paso 1: Información básica del proyecto."""
    
    template_name = 'video_app/wizard/basic_info.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.request.session.get('wizard_project_id')
        
        if project_id:
            project = get_object_or_404(VideoProject, id=project_id)
            context['form'] = ProjectBasicInfoForm(instance=project)
        else:
            context['form'] = ProjectBasicInfoForm()
        
        return context
    
    def post(self, request, *args, **kwargs):
        project_id = request.session.get('wizard_project_id')
        
        if project_id:
            project = get_object_or_404(VideoProject, id=project_id)
            form = ProjectBasicInfoForm(request.POST, instance=project)
        else:
            form = ProjectBasicInfoForm(request.POST)
        
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            request.session['wizard_project_id'] = project.id
            return redirect('video_wizard_template')
        
        return self.render_to_response(self.get_context_data(form=form))

class TemplateSelectionView(VideoWizardView):
    """Paso 2: Selección de template."""
    
    template_name = 'video_app/wizard/template_selection.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TemplateSelectionForm()
        context['templates'] = VideoTemplate.objects.all()
        return context
    
    def get_current_step(self):
        return 2
    
    def post(self, request, *args, **kwargs):
        form = TemplateSelectionForm(request.POST)
        project = get_object_or_404(VideoProject, id=request.session['wizard_project_id'])
        
        if form.is_valid():
            template = form.cleaned_data['template']
            project.template = template
            project.save()
            return redirect('video_wizard_script')
        
        return self.render_to_response(self.get_context_data(form=form))

class ScriptGenerationView(VideoWizardView):
    """Paso 3: Generación y edición de script."""
    
    template_name = 'video_app/wizard/script_generation.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(VideoProject, id=self.request.session['wizard_project_id'])
        
        initial_data = {
            'script': project.script,
            'generate_script': True if not project.script else False
        }
        context['form'] = ScriptGenerationForm(initial=initial_data)
        return context
    
    def get_current_step(self):
        return 3
    
    def post(self, request, *args, **kwargs):
        form = ScriptGenerationForm(request.POST)
        project = get_object_or_404(VideoProject, id=request.session['wizard_project_id'])
        
        if form.is_valid():
            if form.cleaned_data['generate_script']:
                try:
                    service = TextGenerationService()
                    script = service.generate_script(
                        project_title=project.title,
                        project_description=project.description,
                        style=form.cleaned_data['style'],
                        target_duration=form.cleaned_data['target_duration']
                    )
                    project.script = script
                except Exception as e:
                    messages.error(request, f'Error al generar el script: {str(e)}')
            else:
                project.script = form.cleaned_data['script']
            
            project.save()
            return redirect('video_wizard_media')
        
        return self.render_to_response(self.get_context_data(form=form))

class MediaUploadView(VideoWizardView):
    """Paso 4: Subida de medios."""
    
    template_name = 'video_app/wizard/media_upload.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MediaUploadForm()
        return context
    
    def get_current_step(self):
        return 4
    
    def post(self, request, *args, **kwargs):
        form = MediaUploadForm(request.POST, request.FILES)
        project = get_object_or_404(VideoProject, id=request.session['wizard_project_id'])
        
        if form.is_valid():
            if form.cleaned_data['base_media']:
                project.base_media = form.cleaned_data['base_media']
            
            project.save()
            
            # Procesar medios adicionales aquí
            additional_files = request.FILES.getlist('additional_media')
            for file in additional_files:
                # Implementar lógica para manejar archivos adicionales
                pass
            
            return redirect('video_wizard_confirmation')
        
        return self.render_to_response(self.get_context_data(form=form))

class ProjectConfirmationView(VideoWizardView):
    """Paso 5: Confirmación del proyecto."""
    
    template_name = 'video_app/wizard/confirmation.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProjectConfirmationForm()
        context['project'] = get_object_or_404(VideoProject, id=self.request.session['wizard_project_id'])
        return context
    
    def get_current_step(self):
        return 5
    
    def post(self, request, *args, **kwargs):
        form = ProjectConfirmationForm(request.POST)
        project = get_object_or_404(VideoProject, id=request.session['wizard_project_id'])
        
        if form.is_valid():
            if form.cleaned_data['start_processing']:
                project.status = 'processing'
                project.notification_email = form.cleaned_data['notification_email']
                project.save()
                
                # Iniciar el procesamiento asíncrono
                process_video_project.delay(project.id)
                messages.success(request, 'Tu proyecto ha comenzado a procesarse. Te notificaremos cuando esté listo.')
            
            # Limpiar la sesión
            del request.session['wizard_project_id']
            
            return redirect('project_detail', pk=project.id)
        
        return self.render_to_response(self.get_context_data(form=form)) 