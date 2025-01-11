# video_creator
# Sistema de Creación y Edición de Videos con IA

Este proyecto es una aplicación web Django que permite crear y editar videos de manera automatizada utilizando inteligencia artificial. El sistema incluye funcionalidades para procesamiento de video, efectos visuales, y generación de contenido asistido por IA.

## Características Principales

- **Sistema de Plantillas**: Plantillas predefinidas para diferentes tipos de videos (promocionales, educativos, etc.)
- **Efectos de Video**: Biblioteca de efectos visuales incluyendo:
  - Transiciones (fade, slide, zoom)
  - Efectos visuales (blur, brightness, contrast, grayscale)
  - Animaciones de texto y elementos
- **Procesamiento Asíncrono**: Utiliza Celery y Redis para el procesamiento de videos en segundo plano
- **Actualizaciones en Tiempo Real**: WebSockets para mostrar el progreso del procesamiento
- **Interfaz Intuitiva**: Sistema de wizard para guiar al usuario en la creación de videos

## Requisitos Técnicos

- Python 3.8+
- Django 3.2.23
- Redis
- PostgreSQL
- FFmpeg (para procesamiento de video)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/lmrojas/video_creator.git
cd video_creator
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
- Crear archivo `.env` basado en `.env.example`
- Configurar credenciales de base de datos y servicios

5. Aplicar migraciones:
```bash
python manage.py migrate
```

6. Inicializar plantillas:
```bash
python manage.py initialize_templates
```

7. Iniciar servicios:
```bash
# Terminal 1: Servidor Django
python manage.py runserver

# Terminal 2: Worker de Celery
celery -A project_core worker --pool=solo -l info

# Terminal 3: Redis (asegurarse de que Redis esté corriendo)
```

## Estructura del Proyecto

- `project_core/`: Configuración principal del proyecto
- `video_app/`: Aplicación principal
  - `services/`: Servicios de procesamiento de video y efectos
  - `ai_services/`: Servicios de IA para procesamiento de contenido
  - `templates/`: Plantillas HTML
  - `static/`: Archivos estáticos
  - `management/`: Comandos personalizados de Django

## Uso

1. Acceder a la aplicación web
2. Crear un nuevo proyecto de video
3. Seleccionar una plantilla o comenzar desde cero
4. Agregar y editar elementos (texto, imágenes, videos)
5. Aplicar efectos y transiciones
6. Procesar y exportar el video final

## Contribución

Las contribuciones son bienvenidas. Por favor, seguir estos pasos:

1. Fork del repositorio
2. Crear una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
