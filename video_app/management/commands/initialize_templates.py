from django.core.management.base import BaseCommand
from video_app.services.template_manager import TemplateManager

class Command(BaseCommand):
    help = 'Inicializa las plantillas predefinidas de video'

    def handle(self, *args, **options):
        self.stdout.write('Inicializando plantillas predefinidas...')
        
        try:
            TemplateManager.initialize_default_templates()
            self.stdout.write(self.style.SUCCESS('Plantillas inicializadas correctamente'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al inicializar plantillas: {str(e)}')) 