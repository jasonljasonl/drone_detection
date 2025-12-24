from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MavlinkChannelConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('mavlink_group', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('mavlink_group', self.channel_name)

    async def mavlink_message(self,event):
        await self.send(text_data=json.dumps({
            'topic': event['topic'],
            'data': event['data']
        }))