import torch
from TTS.api import TTS
import librosa
import numpy as np
from .base import BaseAIService

class AudioProcessor(BaseAIService):
    """Servicio para procesamiento de audio usando TTS y librosa"""
    
    def __init__(self):
        super().__init__()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.sample_rate = 22050
        self.load_model()
        
    def load_model(self):
        """Carga el modelo TTS"""
        self.tts = TTS(model_name="tts_models/es/css10/vits", progress_bar=False)
        self.tts.to(self.device)
        
    def preprocess(self, input_data):
        """Preprocesa los datos de entrada (texto o audio)"""
        if isinstance(input_data, str):
            return {'type': 'text', 'data': input_data}
        elif isinstance(input_data, np.ndarray):
            return {'type': 'audio', 'data': input_data}
        else:
            raise ValueError("Entrada debe ser texto o array de audio")
            
    def process(self, preprocessed):
        """Procesa los datos según su tipo"""
        if preprocessed['type'] == 'text':
            # Genera audio desde texto
            audio = self.tts.tts(preprocessed['data'])
            return {'audio': audio, 'sample_rate': self.sample_rate}
        else:
            # Analiza características del audio
            audio = preprocessed['data']
            features = {
                'tempo': librosa.beat.tempo(y=audio, sr=self.sample_rate)[0],
                'pitch': librosa.pitch_tuning(y=audio),
                'mfcc': librosa.feature.mfcc(y=audio, sr=self.sample_rate)
            }
            return features
            
    def postprocess(self, results):
        """Postprocesa los resultados"""
        if 'audio' in results:
            return {
                'audio': results['audio'],
                'sample_rate': results['sample_rate'],
                'duration': len(results['audio']) / results['sample_rate']
            }
        else:
            return {
                'tempo': float(results['tempo']),
                'pitch': float(results['pitch']),
                'mfcc_mean': np.mean(results['mfcc'])
            }
            
    def text_to_speech(self, text):
        """Convierte texto a voz"""
        return self.run(text)
        
    def analyze_audio(self, audio_array):
        """Analiza un array de audio"""
        return self.run(audio_array) 