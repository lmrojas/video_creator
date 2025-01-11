# Sistema de creación de videos - Configuración de URLs
# Define todas las rutas disponibles en la aplicación

from django.urls import path
from .views import auth, wizard, dashboard, project

app_name = 'video_app'

urlpatterns = [
    # Rutas de autenticación
    path('register/', auth.RegisterView.as_view(), name='register'),
    
    # Rutas del dashboard
    path('', dashboard.DashboardView.as_view(), name='dashboard'),  # Vista principal
    path('projects/', dashboard.ProjectListView.as_view(), name='project_list'),  # Lista de proyectos
    path('project/<int:pk>/', dashboard.ProjectDetailView.as_view(), name='project_detail'),  # Detalles de proyecto
    
    # Rutas del asistente de creación
    path('wizard/', wizard.WizardStartView.as_view(), name='wizard_start'),  # Inicio del wizard
    path('wizard/step1/', wizard.WizardStep1View.as_view(), name='wizard_step1'),  # Información básica
    path('wizard/step2/', wizard.WizardStep2View.as_view(), name='wizard_step2'),  # Selección de template
    path('wizard/step3/', wizard.WizardStep3View.as_view(), name='wizard_step3'),  # Script
    path('wizard/step4/', wizard.WizardStep4View.as_view(), name='wizard_step4'),  # Subida de medios
    path('wizard/step5/', wizard.WizardStep5View.as_view(), name='wizard_step5'),  # Confirmación
    
    # Rutas de gestión de proyectos
    path('project/<int:pk>/edit/', project.ProjectUpdateView.as_view(), name='project_edit'),  # Edición
    path('project/<int:pk>/delete/', project.ProjectDeleteView.as_view(), name='project_delete'),  # Eliminación
] 