from rest_framework.response import Response
from pymongo.errors import OperationFailure

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import json
import uuid


def addSubcollection(request, client):
    """
    Add a sub-collection to a document in a collection.
    @param request - the request object
    @param client - the client object
    @returns a response object
    """
    data = request.data

    collection_name = data.get('collection_name', None)
    document_id = data.get('document_id', None)
    sub_collection_name = data.get('sub_collection_name', None)
    subdocuments_data = data.get('document_data')
    project_id = data.get('project_id', None)

    # checking 404
    if not project_id:
        return Response({"error": "No project found"}, status=400)
    if not collection_name:
        return Response({"error": "No collection name specified."}, status=400)
    if not sub_collection_name:
        return Response({"error": "No sub collection specified."}, status=400)
    if not subdocuments_data:
        return Response({"error": "No data to add."}, status=400)

    subdocuments_data = json.loads(subdocuments_data)

    # Use the collection name in the URL to select the correct model
    db_store = client.get_database("store")
    db_sub_store = client.get_database("sub_store")

    collection = db_store.get_collection(collection_name)
    sub_collection = db_sub_store.get_collection(sub_collection_name)

    try:
        if collection.count_documents({}) == 0:
            return Response({"error": "Collection not found."}, status=404)
        else:
            subdocuments_data["document_id"] = document_id
            subdocuments_data["collection_id"] = collection_name

            if "_id" not in subdocuments_data:
                subdocuments_data["_id"] = str(uuid.uuid4())

            sub_document = sub_collection.insert_one(subdocuments_data)
            s_id = sub_document.inserted_id

            # Update document instance with the data from the request
            document = collection.update_one(
                {"_id": document_id},
                {"$set": {f"sub_collection_{sub_collection_name}_id": s_id}}
            )
            return Response({"success": True, "message": f"sub-collection created :)"})
    except OperationFailure as e:
        return Response({"success": False, "message": e}, status=500)


def addDocument(request, client):
    """
    Add a document to the specified collection or Create a new collection.
    @param request - the request object           
    @param client - the mongo client           
    @returns a response object           
    """

    data = request.data

    collection_name = data.get('collection_name', None)
    document_data = data.get('document_data', None)
    project_id = data.get('project_id', None)

    # checking 404
    if not project_id:
        return Response({"error": "No project found"}, status=400)
    if not collection_name:
        return Response({"error": "No collection name specified."}, status=400)
    if not document_data:
        return Response({"error": "No data to add."}, status=400)

    document_data = json.loads(document_data)

    # Use the collection name in the URL to select the correct model
    db = client.get_database("store")

    collection = db.get_collection(collection_name)

    try:
        # Create a new document instance with the data from the request
        if "_id" not in document_data:
            document_data["_id"] = str(uuid.uuid4())

        document = collection.insert_one(document_data)

        documents = []
        for doc in collection.find({}).limit(10):
            # Convert BSON document to Python dictionary
            doc_dict = dict(doc)
            # Add the dictionary to the list of documents
            documents.append(doc_dict)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'{project_id}_{collection_name}',
            {
                "type": "websocket.collection",
                "collection": json.dumps(documents)
            })

        return Response({"success": True, "message": f"Inserted document with id: {document.inserted_id}"})

    except OperationFailure as e:
        return Response({"success": False, "message": e}, status=500)


def updateDocument(request, client):
    """
    Update a document in the database.
    @param request - the request object           
    @param client - the database client           
    @returns a response object           
    """
    data = request.data

    collection_name = data.get('collection_name', None)
    document_data = data.get('document_data', None)
    project_id = data.get('project_id', None)

    # checking 404
    if not project_id:
        return Response({"error": "No project found"}, status=400)
    if not collection_name:
        return Response({"error": "No collection name specified."}, status=400)
    if not document_data:
        return Response({"error": "No data to update."}, status=400)

    document_data = json.loads(document_data)
    if "_id" not in document_data.keys():
        return Response({"error": "No document specified."}, status=400)

    document_id = document_data["_id"]

    try:
        db = client.get_database("store")
        collection = db.get_collection(collection_name)
        document_get = collection.find({"_id": document_id})

        if not document_get:
            return Response({"error": "Document not found."}, status=404)

        doc_data_dict = {k: v for k, v in document_data.items() if k != '_id'}

        collection.update_one(
            {"_id": document_id},
            {"$set": doc_data_dict}
        )

        channel_layer = get_channel_layer()
        document_data = collection.find({"_id": document_id})
        document_data = document_data[0]
        document_data = dict(document_data)

        async_to_sync(channel_layer.group_send)(
            f'{project_id}_{collection_name}_{document_id}',
            {
                "type": "websocket.document",
                "document": json.dumps(document_data)
            })

        return Response({"success": True, "message": f"Updated document with id: {document_id}"})

    except OperationFailure as e:
        return Response({"success": False, "message": e}, status=500)


def deleteDocument(request, client, kwargs):
    """
    Delete a document from a collection.
    @param request - the request object           
    @param client - the client object           
    @param kwargs - the keyword arguments           
    @returns the response object           
    """
    if not 'document' in kwargs:
        return Response({"success": False, "message": "No document specified"}, status=404)
    if not 'collection' in kwargs:
        return Response({"success": False, "message": "No collection name specified"}, status=404)

    document_id = kwargs['document']
    collection_name = kwargs['collection']

    try:
        db = client.get_database("store")
        collection = db.get_collection(collection_name)
        response = collection.delete_one({"_id": document_id})
        
        print(response)

        data = request.data
        project_id = data.get('project_id', None)
        

        documents = []
        for doc in collection.find({}).limit(10):
            # Convert BSON document to Python dictionary
            doc_dict = dict(doc)
            # Add the dictionary to the list of documents
            documents.append(doc_dict)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'{project_id}_{collection_name}',
            {
                "type": "websocket.collection",
                "collection": json.dumps(documents)
            })

    except OperationFailure as e:
        return Response({"success": False, "message": e}, status=500)
    
def getDocument(request, client, kwargs):
    """
    Get a document from a collection.
    @param request - the request object           
    @param client - the client object           
    @param kwargs - the keyword arguments           
    @returns the response object           
    """

    data = request.data

    if not 'collection' in data:
        return Response({"success": False, "message": "No collection name specified"}, status=404)

    collection_name = data['collection']
    lookup_field = kwargs['lookup_field']
    lookup_value = kwargs['lookup_value']

    try:
        db = client.get_database("store")
        collection = db.get_collection(collection_name)
        document = collection.find({lookup_field: lookup_value})

        if not document:
            return Response({}, status=200)
        
        document = list(document)

        return Response({"success": True, "message": "Document found", "document": document})

    except OperationFailure as e:
        return Response({"success": False, "message": e}, status=500)