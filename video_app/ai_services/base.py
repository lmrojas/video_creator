from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class BaseAIService(ABC):
    """Clase base para todos los servicios de AI"""
    
    def __init__(self):
        self.model = None
        self.device = None
        
    @abstractmethod
    def load_model(self):
        """Carga el modelo de AI"""
        pass
        
    @abstractmethod
    def preprocess(self, input_data):
        """Preprocesa los datos de entrada"""
        pass
        
    @abstractmethod
    def process(self, preprocessed_data):
        """Procesa los datos usando el modelo"""
        pass
        
    @abstractmethod
    def postprocess(self, model_output):
        """Postprocesa la salida del modelo"""
        pass
        
    def run(self, input_data):
        """Ejecuta el pipeline completo de procesamiento"""
        try:
            preprocessed = self.preprocess(input_data)
            output = self.process(preprocessed)
            result = self.postprocess(output)
            return result
        except Exception as e:
            logger.error(f"Error en el procesamiento: {str(e)}")
            raise

    def cleanup(self):
        """Limpia recursos"""
        if self.model:
            del self.model
            self.model = None 