from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.conf import settings
import jwt
import datetime

class SecurityService:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.token_expiry = datetime.timedelta(days=1)
    
    def authenticate_user(self, username, password):
        """
        Autentica un usuario y retorna un token JWT
        """
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return self._generate_token(user)
            else:
                raise PermissionDenied("Credenciales inválidas")
        except User.DoesNotExist:
            raise PermissionDenied("Usuario no encontrado")
    
    def verify_token(self, token):
        """
        Verifica un token JWT y retorna el usuario
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            return user
        except (jwt.InvalidTokenError, User.DoesNotExist):
            raise PermissionDenied("Token inválido o expirado")
    
    def check_project_permission(self, user, project):
        """
        Verifica si un usuario tiene permiso para acceder a un proyecto
        """
        if project.user == user:
            return True
        raise PermissionDenied("No tienes permiso para acceder a este proyecto")
    
    def _generate_token(self, user):
        """
        Genera un token JWT para un usuario
        """
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.datetime.utcnow() + self.token_expiry
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def validate_content(self, content_type, content):
        """
        Valida el contenido según su tipo
        """
        if content_type == 'video':
            return self._validate_video(content)
        elif content_type == 'image':
            return self._validate_image(content)
        elif content_type == 'text':
            return self._validate_text(content)
        else:
            raise ValueError(f"Tipo de contenido no soportado: {content_type}")
    
    def _validate_video(self, video):
        """
        Valida un archivo de video
        """
        allowed_types = ['video/mp4', 'video/mpeg', 'video/quicktime']
        max_size = 500 * 1024 * 1024  # 500MB
        
        if video.content_type not in allowed_types:
            raise ValueError("Tipo de archivo no permitido")
        
        if video.size > max_size:
            raise ValueError("El archivo excede el tamaño máximo permitido")
        
        return True
    
    def _validate_image(self, image):
        """
        Valida un archivo de imagen
        """
        allowed_types = ['image/jpeg', 'image/png', 'image/gif']
        max_size = 10 * 1024 * 1024  # 10MB
        
        if image.content_type not in allowed_types:
            raise ValueError("Tipo de archivo no permitido")
        
        if image.size > max_size:
            raise ValueError("El archivo excede el tamaño máximo permitido")
        
        return True
    
    def _validate_text(self, text):
        """
        Valida contenido de texto
        """
        max_length = 10000  # 10K caracteres
        
        if len(text) > max_length:
            raise ValueError("El texto excede la longitud máxima permitida")
        
        # TODO: Implementar validación de contenido inapropiado
        
        return True 