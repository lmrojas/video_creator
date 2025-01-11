import json
from channels.generic.websocket import AsyncWebsocketConsumer

class VideoProcessingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Obtener el ID del proyecto de los parámetros de la URL
        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.group_name = f"video_processing_{self.project_id}"

        # Unirse al grupo
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Abandonar el grupo
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Recibe mensajes del WebSocket cliente
        Por ahora solo para debugging
        """
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message', '')
            
            # Echo del mensaje recibido
            await self.send(text_data=json.dumps({
                'type': 'echo',
                'message': f"Recibido: {message}"
            }))
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': "Formato de mensaje inválido"
            }))

    async def processing_update(self, event):
        """
        Maneja las actualizaciones de procesamiento y las envía al cliente
        """
        # Enviar el mensaje al WebSocket
        await self.send(text_data=json.dumps({
            'type': 'processing_update',
            'message': event.get('message', ''),
            'progress': event.get('progress', 0),
            'output_url': event.get('output_url', None)
        })) 