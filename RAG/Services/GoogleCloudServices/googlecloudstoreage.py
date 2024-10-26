import json
from google.cloud import storage
from google.api_core.exceptions import NotFound
from dotenv import load_dotenv

load_dotenv()

class GCPStorageServiceClient:
    def __init__(self):        
        self.bucket_name = "hriti-docs"
        self.client = storage.Client()
        self.bucket = self.client.bucket(self.bucket_name)
        
    # def get_files(self, conversation_id):
        # """
        # Retrieve a files (as a bytestream) from Google Cloud Storage by its conversation_id.
        # The conversation is stored as a JSON string.
        # """
        # blob_name = f"conversation-{conversation_id}.json"
        # blob = self.bucket.blob(blob_name)
        # try:
        #     # Download the JSON data from the blob
        #     blob_data = blob.download_as_text()
        #     # Deserialize the JSON string into a list of dictionaries (JSON objects)
        #     conversations = json.loads(blob_data)
        #     return conversations
        # except NotFound:
        #     print(f"Conversation with ID {conversation_id} not found.")
        #     return None
        # except Exception as e:
        #     print(f"Error retrieving conversation: {str(e)}")
        #     return None

    async def add_files(self, app_id, filename, file) -> str:
        """
        Add a file to Google Cloud Storage. The file is expected to be a bytestream file
        """
        blob_name = f"{app_id}/{filename}"
        blob = self.bucket.blob(blob_name)
        try:   
            await file.seek(0)    
            file_bytes = await file.read()     
            if not file_bytes:
                raise ValueError("File is empty or could not be read correctly.")            
            blob.upload_from_string(file_bytes, content_type = 'application/pdf')
            blob.make_public()            
            print(f"file with file name {filename} successfully uploaded.")
            return blob.public_url
        except Exception as e:
            print(f"Error uploading file: {str(e)}")
            return "Error"

    # def delete_files(self, conversation_id):
        # """
        # Delete a conversation from Google Cloud Storage by its conversation_id.
        # """
        # blob_name = f"conversation-{conversation_id}.json"
        # blob = self.bucket.blob(blob_name)
        # try:
        #     blob.delete()
        #     print(f"Conversation with ID {conversation_id} successfully deleted.")
        # except NotFound:
        #     print(f"Conversation with ID {conversation_id} not found.")
        # except Exception as e:
        #     print(f"Error deleting conversation: {str(e)}")

