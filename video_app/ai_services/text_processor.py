from transformers import pipeline
import torch
from .base import BaseAIService

class TextProcessor(BaseAIService):
    """Servicio para procesamiento de texto usando transformers"""
    
    def __init__(self):
        super().__init__()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.load_model()
        
    def load_model(self):
        """Carga el modelo de procesamiento de texto"""
        self.summarizer = pipeline("summarization", device=self.device)
        self.translator = pipeline("translation", model="Helsinki-NLP/opus-mt-es-en", device=self.device)
        self.sentiment = pipeline("sentiment-analysis", device=self.device)
        
    def preprocess(self, text):
        """Preprocesa el texto de entrada"""
        if not isinstance(text, str):
            raise ValueError("La entrada debe ser una cadena de texto")
        return text.strip()
        
    def process(self, text):
        """Procesa el texto usando los modelos cargados"""
        results = {
            'summary': self.summarizer(text, max_length=130, min_length=30, do_sample=False),
            'translation': self.translator(text),
            'sentiment': self.sentiment(text)
        }
        return results
        
    def postprocess(self, results):
        """Postprocesa los resultados del modelo"""
        return {
            'summary': results['summary'][0]['summary_text'],
            'translation': results['translation'][0]['translation_text'],
            'sentiment': results['sentiment'][0]['label'],
            'confidence': results['sentiment'][0]['score']
        }
        
    def analyze_script(self, script):
        """Analiza un guión completo"""
        return self.run(script) 