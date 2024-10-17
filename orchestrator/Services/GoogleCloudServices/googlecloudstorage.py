import json
from google.cloud import storage
from google.api_core.exceptions import NotFound
import os
from dotenv import load_dotenv

load_dotenv()

class GCPStorageServiceClient:
    def __init__(self):        
        self.bucket_name = "hriti-conversations-bucket"
        self.client = storage.Client()
        self.bucket = self.client.bucket(self.bucket_name)
        
    def get_conversations(self, conversation_id):
        """
        Retrieve a conversation (as a list of JSON objects) from Google Cloud Storage by its conversation_id.
        The conversation is stored as a JSON string.
        """
        blob_name = f"conversation-{conversation_id}.json"
        blob = self.bucket.blob(blob_name)
        try:
            # Download the JSON data from the blob
            blob_data = blob.download_as_text()
            # Deserialize the JSON string into a list of dictionaries (JSON objects)
            conversations = json.loads(blob_data)
            return conversations
        except NotFound:
            print(f"Conversation with ID {conversation_id} not found.")
            return None
        except Exception as e:
            print(f"Error retrieving conversation: {str(e)}")
            return None

    def add_conversation(self, conversation_id, conversations):
        """
        Add a conversation to Google Cloud Storage. The conversation is expected to be a list of JSON objects.
        The list of JSON objects is serialized into a JSON string before storing.
        If a conversation with the same ID already exists, it will be overwritten.
        """
        blob_name = f"conversation-{conversation_id}.json"
        blob = self.bucket.blob(blob_name)
        try:
            # Serialize the list of JSON objects (dictionaries) to a JSON string
            conversation_data = json.dumps(conversations)
            # Upload the serialized data to Google Cloud Storage, overwrite if exists
            blob.upload_from_string(conversation_data, content_type='application/json')
            print(f"Conversation with ID {conversation_id} successfully uploaded.")
        except Exception as e:
            print(f"Error uploading conversation: {str(e)}")

    def delete_conversation(self, conversation_id):
        """
        Delete a conversation from Google Cloud Storage by its conversation_id.
        """
        blob_name = f"conversation-{conversation_id}.json"
        blob = self.bucket.blob(blob_name)
        try:
            blob.delete()
            print(f"Conversation with ID {conversation_id} successfully deleted.")
        except NotFound:
            print(f"Conversation with ID {conversation_id} not found.")
        except Exception as e:
            print(f"Error deleting conversation: {str(e)}")

