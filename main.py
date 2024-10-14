from ingestion_api_gcs.ingestion import Ingestion
from ingestion_api_gcs.storage import Storage


ingest = Ingestion('fca_live_XIVoblWj0cgSenelNf9rsWGaKPZYsqyXULfIL3ub')
json_file = ingest.taxa_cambio('BRL')

cliente = Storage()
cliente.upload_json_memory(json_file, 'datalake-mvsh-export', 'raw/teste.json')