from google.cloud.storage import Client
from google.cloud.secretmanager import SecretManagerServiceClient
from typing import TypeVar
import os
import json

GsClient = TypeVar(
    'GsClient', 
    Client, 
    SecretManagerServiceClient
)

class Cred:
    def __init__(
        self,
        client: GsClient,
        credentials: str = None
    ) -> None:
        
        self.client = client
        self.credentials = credentials
    
    def get_cliente(self) -> GsClient:
        if self.credentials:

            if all(
                [
                    os.path.isfile(self.credentials),
                    self.credentials.endswith('.json')
                ]
            ):
               return self.client.from_service_account_json(self.credentials)

            json_loads = json.loads(self.credentials)
            return self.client.from_service_account_info(json_loads)
        
        return self.client()