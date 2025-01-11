from transformers import pipeline
from django.conf import settings
import torch

class TextGenerationService:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.generator = pipeline(
            'text-generation',
            model='gpt2-medium',
            device=self.device
        )

    def generate_script(self, prompt, max_length=500):
        """
        Genera un script basado en el prompt proporcionado
        """
        try:
            generated_text = self.generator(
                prompt,
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.7,
                top_k=50,
                top_p=0.95
            )[0]['generated_text']
            
            # Limpiamos el texto generado
            script = generated_text.replace(prompt, '').strip()
            return script
        except Exception as e:
            print(f"Error en la generación de texto: {str(e)}")
            return None

    def generate_description(self, title, target_audience, max_length=200):
        """
        Genera una descripción para el video
        """
        prompt = f"Genera una descripción atractiva para un video titulado '{title}' "
        prompt += f"dirigido a {target_audience}:"
        
        try:
            description = self.generator(
                prompt,
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.7
            )[0]['generated_text']
            
            return description.replace(prompt, '').strip()
        except Exception as e:
            print(f"Error en la generación de descripción: {str(e)}")
            return None

    def suggest_improvements(self, script):
        """
        Sugiere mejoras para un script existente
        """
        prompt = f"Analiza el siguiente script y sugiere mejoras:\n{script}\n\nMejoras sugeridas:"
        
        try:
            suggestions = self.generator(
                prompt,
                max_length=len(prompt) + 300,
                num_return_sequences=1,
                temperature=0.8
            )[0]['generated_text']
            
            return suggestions.split("Mejoras sugeridas:")[1].strip()
        except Exception as e:
            print(f"Error al generar sugerencias: {str(e)}")
            return None 