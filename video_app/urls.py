# Sistema de creación de videos - Configuración de URLs
# Define todas las rutas disponibles en la aplicación

from django.urls import path
from .views import auth, dashboard
from .views.wizard import (
    ProjectBasicInfoView,
    TemplateSelectionView,
    ScriptGenerationView,
    MediaUploadView,
    ProjectConfirmationView
)
from .views.editor import SceneEditorView

app_name = 'video_app'

urlpatterns = [
    # Rutas del dashboard
    path('', dashboard.DashboardView.as_view(), name='dashboard'),
    path('projects/', dashboard.ProjectListView.as_view(), name='project_list'),
    path('project/<int:pk>/', dashboard.ProjectDetailView.as_view(), name='project_detail'),
    
    # Rutas del asistente de creación
    path('wizard/basic-info/', ProjectBasicInfoView.as_view(), name='video_wizard_basic_info'),
    path('wizard/template/', TemplateSelectionView.as_view(), name='video_wizard_template'),
    path('wizard/script/', ScriptGenerationView.as_view(), name='video_wizard_script'),
    path('wizard/media/', MediaUploadView.as_view(), name='video_wizard_media'),
    path('wizard/confirmation/', ProjectConfirmationView.as_view(), name='video_wizard_confirmation'),
    
    # Rutas del editor
    path('project/<int:project_id>/scene/<int:scene_id>/edit/', 
         SceneEditorView.as_view(), 
         name='scene_editor'),
] 