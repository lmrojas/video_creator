from django import forms
from .models import AudioElement
from .ai_services.tts import TTSService

class TTSGenerationForm(forms.Form):
    """Formulario para generar audio usando Text-to-Speech."""
    
    text_content = forms.CharField(
        label='Texto a convertir',
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'})
    )
    
    voice_id = forms.ChoiceField(
        label='Voz',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    start_time = forms.FloatField(
        label='Tiempo de inicio (segundos)',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    
    end_time = forms.FloatField(
        label='Tiempo de fin (segundos)',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    
    volume = forms.FloatField(
        label='Volumen',
        min_value=0,
        max_value=1,
        initial=1.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtener las voces disponibles del servicio TTS
        tts_service = TTSService()
        voices = tts_service.get_available_voices()
        self.fields['voice_id'].choices = [
            (voice['id'], f"{voice['name']} ({voice['gender']})") 
            for voice in voices
        ] 