from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer

import json

from mongoengine import connect, disconnect
from pymongo.errors import OperationFailure

client = connect(
    host="mongodb+srv://jatin21ai:wZMjBcTb2No6TpRO@cluster1.bxuv5nq.mongodb.net/?retryWrites=true&w=majority", name="store")


class CollectionSubscribeSyncConsumerApi(AsyncConsumer):
    """
    This is the consumer for the websocket. It subscribes to a collection, it does'nt listens for messages.
    @param event - the event that is recieved from the websocket.
    """
    async def websocket_connect(self, event):
        print("websocket Connected...")

        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.collection_name = self.scope['url_route']['kwargs']['collection_name']

        self.group_name = f'{self.project_id}_{self.collection_name}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        db = client.get_database("store")
        collection = db.get_collection(self.collection_name)

        documents = []
        for doc in collection.find({}).limit(10):
            # Convert BSON document to Python dictionary
            doc_dict = dict(doc)
            # Add the dictionary to the list of documents
            documents.append(doc_dict)

        await self.send({
            'type': 'websocket.accept',
        })

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'websocket.collection',
                'collection': json.dumps(documents)
            })

    def websocket_disconnect(self, event):
        print("websocket Disconnected...", event)
        disconnect()
        raise StopConsumer()

    async def websocket_collection(self, event):
        documents = event['collection']
        print('here event call')
        await self.send({
            'type': 'websocket.send',
            'text': documents
        })


class DocumentSubscribeSyncConsumerApi(AsyncConsumer):
    """
    When the websocket is connected, send the document to the group.
    @param event - the websocket event
    """
    async def websocket_connect(self, event):
        print("websocket Connected...", event)

        self.document_id = self.scope['url_route']['kwargs']['document_id']
        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.collection_name = self.scope['url_route']['kwargs']['collection_name']

        self.group_name = f'{self.project_id}_{self.collection_name}_{self.document_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.send({
            'type': 'websocket.accept'
        })

        try:
            db = client.get_database("store")
            collection = db.get_collection(self.collection_name)

            document = collection.find({"_id": self.document_id})

            if document:
                document = document[0]
            # Convert BSON document to Python dictionary
            doc_dict = dict(document)

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'websocket.document',
                    'document': json.dumps(doc_dict)
                })
        except:
            await self.send({
                'type': 'websocket.send',
                'text': "something went wrong :( "
            })

    def websocket_disconnect(self, event):
        print("websocket Disconnected...", event)
        disconnect()
        raise StopConsumer()

    async def websocket_document(self, event):
        document = event['document']
        print('here event call')
        await self.send({
            'type': 'websocket.send',
            'text': document
        })


class SyncConsumerApi(SyncConsumer):

    def websocket_connect(self, event):
        print("websocket Connected...", event)

        print("Channel Layer", self.channel_layer)
        print("Channel Name", self.channel_name)

        print(self.scope, 'scope here')
        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        print("websocket Recived...", type(event['text']))

        self.send({
            'type': 'websocket.send',
            'text': json.dumps({"json_msg": 'message from server'})
        })

    def websocket_disconnect(self, event):
        print("websocket Disconnected...", event)

        raise StopConsumer()


class AsyncConsumerApi(AsyncConsumer):

    async def websocket_connect(self, event):
        print("websocket Connected...", event)

    async def websocket_recive(self, event):
        print("websocket Reciveed...", event)

    async def websocket_disconnect(self, event):
        print("websocket Disconnected...", event)
