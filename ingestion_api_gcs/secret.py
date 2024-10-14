from google.cloud.secretmanager import (
    SecretManagerServiceClient,
    AccessSecretVersionResponse
)
import google_crc32c
from cred import (
    Cred, 
    GsClient
)


class Secret(Cred):
    def __init__(
        self, 
        project_id: str, 
        secret_id: str, 
        version_id: int = 1,
        client: GsClient = SecretManagerServiceClient, 
        credentials: str = None
    ) -> None:
        
        super().__init__(client, credentials)
        self.name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    
    def access_secret_version(self) -> AccessSecretVersionResponse:
        
        client = self.get_cliente()
        response = client.access_secret_version(request={"name": self.name})

        crc32c = google_crc32c.Checksum()
        crc32c.update(response.payload.data)
        if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
            print("[ERROR] Service Secret-Key.")
            return response

        payload = response.payload.data.decode("UTF-8")

        return payload