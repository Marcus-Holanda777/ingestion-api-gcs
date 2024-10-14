from google.cloud.storage import Client, Blob
import json
import os


class Storage:
    def __init__(self, credentials = None) -> None:
        self.credentials = credentials
    
    def __get_cliente(self) -> Client:
        if self.credentials:

            if all(
                [
                    os.path.isfile(self.credentials),
                    self.credentials.endswith('.json')
                ]
            ):
               return Client.from_service_account_json(self.credentials)

            json_loads = json.loads(self.credentials)
            return Client.from_service_account_info(json_loads)
        
        return Client()

    def upload_json_memory(
        self,
        data,
        bucket_name: str,
        blob_name: str
    ) -> Blob:
        
        cliente = self.__get_cliente()
        bucket = cliente.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        blob.upload_from_string(
            data=json.dumps(data, indent=4),
            content_type='application/json'
        )

        return blob