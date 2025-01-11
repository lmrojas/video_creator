import os
from celery import Celery

# Establecer la configuración de Django por defecto para celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_core.settings')

# Crear la aplicación Celery
app = Celery('project_core')

# Usar la configuración de Django para la configuración de Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Cargar tareas automáticamente de todas las aplicaciones registradas
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}') 