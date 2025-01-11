from transformers import pipeline
import torch
from moviepy.editor import VideoFileClip
import os
from django.conf import settings

class VideoAnalyzer:
    def __init__(self):
        self.image_classifier = pipeline("image-classification")
        self.text_classifier = pipeline("text-classification")
        
    def analyze_video(self, video_path):
        """
        Analiza el contenido de un video y retorna información relevante
        """
        try:
            video = VideoFileClip(video_path)
            
            # Analizar frames clave
            frame_analysis = self._analyze_frames(video)
            
            # Analizar texto/script si existe
            text_analysis = self._analyze_text(video_path)
            
            return {
                'status': 'success',
                'frame_analysis': frame_analysis,
                'text_analysis': text_analysis
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _analyze_frames(self, video):
        """
        Analiza frames clave del video para identificar contenido
        """
        results = []
        duration = video.duration
        
        # Analizar un frame cada 5 segundos
        for t in range(0, int(duration), 5):
            frame = video.get_frame(t)
            analysis = self.image_classifier(frame)
            results.append({
                'time': t,
                'predictions': analysis
            })
            
        return results
    
    def _analyze_text(self, video_path):
        """
        Analiza el texto/script asociado al video
        """
        # TODO: Implementar extracción de texto del video
        # Por ahora, retornar un análisis básico
        return {
            'sentiment': 'positive',
            'topics': ['technology', 'education'],
            'language': 'es'
        }
    
    def get_recommendations(self, analysis_results):
        """
        Genera recomendaciones basadas en el análisis del video
        """
        recommendations = []
        
        # Analizar resultados de frames
        if 'frame_analysis' in analysis_results:
            for frame in analysis_results['frame_analysis']:
                if frame['predictions']:
                    recommendations.append({
                        'type': 'visual',
                        'time': frame['time'],
                        'suggestion': f"Considerar ajustar el contenido visual en {frame['time']} segundos"
                    })
        
        # Analizar resultados de texto
        if 'text_analysis' in analysis_results:
            text_analysis = analysis_results['text_analysis']
            if text_analysis['sentiment'] == 'negative':
                recommendations.append({
                    'type': 'content',
                    'suggestion': "Considerar revisar el tono del contenido para hacerlo más positivo"
                })
        
        return recommendations 