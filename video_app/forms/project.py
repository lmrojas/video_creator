from django import forms
from ..models import VideoProject, AudioElement

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

class TTSGenerationForm(forms.ModelForm):
    """Formulario para generar audio usando TTS."""
    
    class Meta:
        model = AudioElement
        fields = ['text_content', 'voice_id', 'start_time', 'end_time', 'volume']
        widgets = {
            'text_content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ingrese el texto que desea convertir a voz...'
            }),
            'voice_id': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0'
            }),
            'end_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0'
            }),
            'volume': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'max': '2'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['voice_id'].widget.choices = [
            ('es_female', 'Español (Mujer)'),
            ('en_female', 'Inglés (Mujer)')
        ]
        self.fields['voice_id'].label = 'Voz'
        self.fields['text_content'].label = 'Texto'
        self.fields['start_time'].label = 'Tiempo de inicio (segundos)'
        self.fields['end_time'].label = 'Tiempo de fin (segundos)'
        self.fields['volume'].label = 'Volumen (0.0 - 2.0)' 