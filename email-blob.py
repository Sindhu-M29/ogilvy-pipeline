import imaplib
import email
from azure.storage.blob import BlobServiceClient, BlobClient
import os
import tempfile
import zipfile
import io

# Email Configuration
EMAIL_HOST = 'imap.gmail.com'
EMAIL_USERNAME = 'sindhu.ilango@pennywisesolutions.com'
EMAIL_FOLDER = 'INBOX'
SUBJECT_KEYWORD = 'Ogilvy-latest-deployments'

# Azure Storage Configuration
STORAGE_CONNECTION_STRING = os.getenv('STORAGE_CONNECTION_STRING')
CONTAINER_NAME = 'attachments'

# Connect to Azure Storage Account
blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# Connect to Email Server
mail = imaplib.IMAP4_SSL(EMAIL_HOST)
mail.login(EMAIL_USERNAME)
mail.select(EMAIL_FOLDER)

# Search for emails with specific subject
result, data = mail.search(None, f'(UNSEEN SUBJECT "{SUBJECT_KEYWORD}")')
if result == 'OK':
    for num in data[0].split():
        result, message_data = mail.fetch(num, '(RFC822)')
        if result == 'OK':
            email_message = email.message_from_bytes(message_data[0][1])
            for part in email_message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                filename = part.get_filename()
                if filename.endswith('.zip'):
                    # Download zip attachment
                    zip_data = part.get_payload(decode=True)

                    # Upload zip attachment to Azure Blob Storage
                    zip_blob_name = webapp
                    zip_blob_client = container_client.get_blob_client(zip_blob_name)
                    zip_blob_client.upload_blob(zip_data)

                    # Extract zip attachment
                    with zipfile.ZipFile(io.BytesIO(zip_data), 'r') as zip_ref:
                        # Upload extracted files to Azure Blob Storage
                        for zip_info in zip_ref.infolist():
                            with zip_ref.open(zip_info.filename) as file:
                                extracted_blob_name = f"{filename[:-4]}/{zip_info.filename}"
                                extracted_blob_client = container_client.get_blob_client(extracted_blob_name)
                                extracted_blob_client.upload_blob(file)

# Disconnect from Email Server
mail.close()
mail.logout()
