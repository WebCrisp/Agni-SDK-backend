from rest_framework.views import APIView
from mongoengine import Document, EmbeddedDocument, fields
from mongoengine import StringField, IntField, FloatField, DateTimeField, ListField, DictField
from rest_framework.response import Response

from authentication.utils import APIKeyAuthentication, ProjectPermission
import json

from mongoengine import connect, disconnect

from . import helper

client = connect(host="mongodb+srv://jatin21ai:wZMjBcTb2No6TpRO@cluster1.bxuv5nq.mongodb.net/?retryWrites=true&w=majority", name="store")

class AddSubCollectionAPIView(APIView):

    authentication_classes = [APIKeyAuthentication]
    permission_classes = [ProjectPermission]

    def post(self, request, *args, **kwargs):
        response = helper.addSubcollection(request, client)
        return response


class DocumentAPIView(APIView):

    authentication_classes = [APIKeyAuthentication]
    permission_classes = [ProjectPermission]

    def get(self, request, *args, **kwargs):
        response = helper.getDocument(request, client, kwargs)
        return response

    def post(self, request, *args, **kwargs):
        response = helper.addDocument(request, client)
        return response
    
    def put(self, request, *args, **kwargs):
        response = helper.updateDocument(request, client)
        return response
    
    def delete(self, request, *args, **kwargs):
        response = helper.deleteDocument(request, client, kwargs)
        return response