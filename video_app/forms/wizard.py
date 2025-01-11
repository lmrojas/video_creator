from django import forms
from ..models import VideoProject, VideoTemplate

class ProjectBasicForm(forms.ModelForm):
    """Formulario para información básica del proyecto"""
    class Meta:
        model = VideoProject
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Título del video'}),
            'description': forms.Textarea(attrs={'placeholder': 'Descripción del video', 'rows': 4})
        }

class TemplateSelectionForm(forms.ModelForm):
    """Formulario para selección de plantilla"""
    template = forms.ModelChoiceField(
        queryset=VideoTemplate.objects.all(),
        empty_label="Selecciona una plantilla",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = VideoProject
        fields = ['template']

class ScriptForm(forms.ModelForm):
    """Formulario para el script del video"""
    class Meta:
        model = VideoProject
        fields = ['script']
        widgets = {
            'script': forms.Textarea(attrs={
                'placeholder': 'Escribe el guión de tu video aquí...',
                'rows': 10
            })
        }

class MediaForm(forms.ModelForm):
    """Formulario para subida de medios"""
    class Meta:
        model = VideoProject
        fields = ['base_media']
        widgets = {
            'base_media': forms.FileInput(attrs={'accept': 'image/*,video/*,audio/*'})
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