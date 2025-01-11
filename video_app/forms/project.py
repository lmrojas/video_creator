from django import forms
from ..models import VideoProject

class VideoProjectForm(forms.ModelForm):
    """Formulario para edición de proyectos"""
    class Meta:
        model = VideoProject
        fields = ['title', 'description', 'script', 'base_media', 'template']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'script': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'base_media': forms.FileInput(attrs={'class': 'form-control'}),
            'template': forms.Select(attrs={'class': 'form-select'})
        }
    
    def clean_base_media(self):
        """Validar el archivo subido"""
        media = self.cleaned_data.get('base_media')
        if media:
            # Validar tamaño (máximo 100MB)
            if media.size > 100 * 1024 * 1024:
                raise forms.ValidationError('El archivo no puede ser mayor a 100MB')
            
            # Validar tipo de archivo
            content_type = media.content_type.split('/')[0]
            if content_type not in ['image', 'video', 'audio']:
                raise forms.ValidationError('Tipo de archivo no permitido')
        
        return media 