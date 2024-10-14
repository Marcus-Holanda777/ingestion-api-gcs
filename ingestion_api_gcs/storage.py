from google.cloud.storage import (
    Client, 
    Blob
)
import json
from typing import Any
from cred import Cred, GsClient


class Storage(Cred):
    def __init__(
        self, 
        client: GsClient = Client,
        credentials: str = None
    ) -> None:
        
        super().__init__(client, credentials)

    def upload_json_memory(
        self,
        data: Any,
        bucket_name: str,
        blob_name: str
    ) -> Blob:
        
        cliente = self.get_cliente()
        bucket = cliente.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        blob.upload_from_string(
            data=json.dumps(data, indent=4),
            content_type='application/json'
        )

        return blob