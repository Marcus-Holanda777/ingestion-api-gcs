from secret import Secret
from storage import Storage
from ingestion import Ingestion
import os
from datetime import datetime


project_id = os.getenv('project_id')
secret_id = os.getenv('secret_id')
bucket_name = os.getenv('bucket_name')


def insert_json(request):
    
    # NOTE: Retorna TOKEN de acesso a API
    segredo = Secret(project_id, secret_id)
    token = segredo.access_secret_version()

    # NOTE: Download do arquivo -- moeda BRL
    # em relacao as outras moedas
    api_ingestion = Ingestion(token)
    data = api_ingestion.taxa_cambio(base_currency='BRL')

    # NOTE: Enviar os dados para o bucket
    bucket = Storage()
    file_to = f'{datetime.now():%Y%m%d_%H%M}'
    bucket.upload_json_memory(data, bucket_name, f'raw/{file_to}')

    return "OK"