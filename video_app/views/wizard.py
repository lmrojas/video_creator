# Sistema de creación de videos - Módulo de Wizard
# Implementa un asistente paso a paso para la creación de videos

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from ..models import VideoProject, VideoTemplate
from ..forms.wizard import ProjectBasicForm, TemplateSelectionForm, ScriptForm, MediaForm

class WizardBaseMixin:
    """Mixin base para las vistas del wizard"""
    def dispatch(self, request, *args, **kwargs):
        # Verificar si hay un proyecto en progreso
        project_id = request.session.get('wizard_project_id')
        if not project_id and self.step > 1:
            return redirect('video_app:wizard_start')
        return super().dispatch(request, *args, **kwargs)

class WizardStartView(LoginRequiredMixin, TemplateView):
    """Vista inicial del wizard"""
    template_name = 'video_app/wizard/start.html'
    
    def get(self, request, *args, **kwargs):
        # Limpiar datos del wizard anterior
        if 'wizard_project_id' in request.session:
            del request.session['wizard_project_id']
        return super().get(request, *args, **kwargs)

class WizardStep1View(LoginRequiredMixin, WizardBaseMixin, TemplateView):
    """Paso 1: Información básica del proyecto"""
    template_name = 'video_app/wizard/step1.html'
    step = 1
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProjectBasicForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = ProjectBasicForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            request.session['wizard_project_id'] = project.id
            return redirect('video_app:wizard_step2')
        return self.render_to_response({'form': form})

class WizardStep2View(LoginRequiredMixin, WizardBaseMixin, TemplateView):
    """Paso 2: Selección de plantilla"""
    template_name = 'video_app/wizard/step2.html'
    step = 2
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TemplateSelectionForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = TemplateSelectionForm(request.POST)
        if form.is_valid():
            project = VideoProject.objects.get(id=request.session['wizard_project_id'])
            project.template = form.cleaned_data['template']
            project.save()
            return redirect('video_app:wizard_step3')
        return self.render_to_response({'form': form})

class WizardStep3View(LoginRequiredMixin, WizardBaseMixin, TemplateView):
    """Paso 3: Script del video"""
    template_name = 'video_app/wizard/step3.html'
    step = 3
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = VideoProject.objects.get(id=self.request.session['wizard_project_id'])
        context['form'] = ScriptForm(instance=project)
        return context
    
    def post(self, request, *args, **kwargs):
        project = VideoProject.objects.get(id=request.session['wizard_project_id'])
        form = ScriptForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('video_app:wizard_step4')
        return self.render_to_response({'form': form})

class WizardStep4View(LoginRequiredMixin, WizardBaseMixin, TemplateView):
    """Paso 4: Subida de medios"""
    template_name = 'video_app/wizard/step4.html'
    step = 4
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = VideoProject.objects.get(id=self.request.session['wizard_project_id'])
        context['form'] = MediaForm(instance=project)
        return context
    
    def post(self, request, *args, **kwargs):
        project = VideoProject.objects.get(id=request.session['wizard_project_id'])
        form = MediaForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('video_app:wizard_step5')
        return self.render_to_response({'form': form})

class WizardStep5View(LoginRequiredMixin, WizardBaseMixin, TemplateView):
    """Paso 5: Confirmación"""
    template_name = 'video_app/wizard/step5.html'
    step = 5
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = VideoProject.objects.get(id=self.request.session['wizard_project_id'])
        context['project'] = project
        return context
    
    def post(self, request, *args, **kwargs):
        project = VideoProject.objects.get(id=request.session['wizard_project_id'])
        project.status = 'processing'
        project.save()
        del request.session['wizard_project_id']
        return redirect('video_app:project_detail', pk=project.id) 