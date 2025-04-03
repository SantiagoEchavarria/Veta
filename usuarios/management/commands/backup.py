from django.core.management.base import BaseCommand
from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from cryptography.fernet import Fernet
import datetime
import os

# Configuración
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = os.path.join(settings.BASE_DIR, 'service-account.json')  # Ruta a tu JSON
FOLDER_ID = '1vsN1UnmeZ508zbQ0HYNhMZA9eYV_K8QJ' 

class Command(BaseCommand):
    help = 'Backup cifrado con cuenta de servicio'

    def handle(self, *args, **options):
        # 1. Cifrar DB
        db_path = settings.DATABASES['default']['NAME']
        backup_name = f"backup-{datetime.datetime.now().strftime('%Y-%m-%d')}.db.enc"
        key = Fernet.generate_key()

        with open(db_path, 'rb') as f:
            data = Fernet(key).encrypt(f.read())

        with open(backup_name, 'wb') as f:
            f.write(data)

        # 2. Autenticación
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = build('drive', 'v3', credentials=credentials)

        # 3. Subir archivo
        file_metadata = {
            'name': backup_name,
            'parents': [FOLDER_ID]
        }
        media = MediaFileUpload(backup_name, mimetype='application/octet-stream')
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        self.stdout.write(self.style.SUCCESS(f'Backup subido: {file.get("id")}'))

        # 4. Guardar clave (en lugar seguro)
        with open(f'clave_{backup_name}.key', 'wb') as f:
            f.write(key)