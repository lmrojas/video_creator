from django import forms
from ..models import VideoProject, VideoTemplate, TEMPLATE_CATEGORIES, DIFFICULTY_LEVELS
from ..widgets import MultipleFileInput

class ProjectBasicInfoForm(forms.ModelForm):
    """Formulario para el paso 1: Información básica del proyecto."""
    
    class Meta:
        model = VideoProject
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el título de su video'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describa el propósito y contenido de su video'
            })
        }

class TemplateSelectionForm(forms.Form):
    """Formulario para el paso 2: Selección de template."""
    
    template = forms.ModelChoiceField(
        queryset=VideoTemplate.objects.all(),
        empty_label="Seleccione un template",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    category = forms.ChoiceField(
        choices=[('', 'Todas las categorías')] + TEMPLATE_CATEGORIES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    difficulty_level = forms.ChoiceField(
        choices=[('', 'Todos los niveles')] + DIFFICULTY_LEVELS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['template'].queryset = VideoTemplate.objects.order_by('name')

class ScriptGenerationForm(forms.Form):
    """Formulario para el paso 3: Generación y edición de script."""
    
    generate_script = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    style = forms.ChoiceField(
        choices=[
            ('dynamic', 'Dinámico'),
            ('professional', 'Profesional'),
            ('creative', 'Creativo'),
            ('educational', 'Educativo'),
            ('emotional', 'Emocional')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    target_duration = forms.IntegerField(
        min_value=30,
        max_value=600,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Duración en segundos'
        })
    )
    
    script = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 10,
            'placeholder': 'El script se generará automáticamente o puede escribirlo manualmente'
        }),
        required=False
    )

class MediaUploadForm(forms.Form):
    """Formulario para el paso 4: Subida de medios."""
    
    base_media = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': 'video/*,image/*'
        })
    )
    
    additional_media = forms.FileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': 'video/*,image/*,audio/*'
        })
    )
    
    def clean_base_media(self):
        media = self.cleaned_data.get('base_media')
        if media:
            if media.size > 100 * 1024 * 1024:  # 100MB
                raise forms.ValidationError('El archivo no puede ser mayor a 100MB')
            
            content_type = media.content_type.split('/')[0]
            if content_type not in ['video', 'image']:
                raise forms.ValidationError('Tipo de archivo no permitido')
        return media
    
    def clean_additional_media(self):
        files = self.files.getlist('additional_media')
        for media in files:
            if media.size > 50 * 1024 * 1024:  # 50MB
                raise forms.ValidationError(f'El archivo {media.name} no puede ser mayor a 50MB')
            
            content_type = media.content_type.split('/')[0]
            if content_type not in ['video', 'image', 'audio']:
                raise forms.ValidationError(f'Tipo de archivo no permitido: {media.name}')
        return files

class ProjectConfirmationForm(forms.Form):
    """Formulario para el paso 5: Confirmación del proyecto."""
    
    terms_accepted = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        error_messages={'required': 'Debe aceptar los términos y condiciones'}
    )
    
    start_processing = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    notification_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo para notificaciones (opcional)'
        })
    ) 