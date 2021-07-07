from config import config
from azure.storage.blob import BlobServiceClient

def get_blob_service():
    return BlobServiceClient.from_connection_string(
        config['azure']['connection'])

def get_blob_container(container):
    blob_service_client = get_blob_service()
    return blob_service_client.get_container_client(container)

def get_blob_client(container, file):
    container_client = get_blob_container(container)
    return container_client.get_blob_client(file)
