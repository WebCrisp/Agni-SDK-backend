from django.urls import path
from .import consumers

websocket_urls = [
    path('ws/sc/', consumers.SyncConsumerApi.as_asgi()),
    path('ws/collection/<str:project_id>/<str:collection_name>/', consumers.CollectionSubscribeSyncConsumerApi.as_asgi()),
    path('ws/document/<str:project_id>/<str:collection_name>/<str:document_id>/', consumers.DocumentSubscribeSyncConsumerApi.as_asgi()),
    path('ws/ac/', consumers.AsyncConsumerApi.as_asgi()),   
]