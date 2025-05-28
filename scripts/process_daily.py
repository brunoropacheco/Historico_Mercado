import os
import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
import io
import logging
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Directory where images will be stored
IMAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'images')

# Create directories if they don't exist
os.makedirs(IMAGE_DIR, exist_ok=True)

# Path to store the timestamp of last check
LAST_CHECK_FILE = os.path.join(os.path.dirname(__file__), 'last_check.txt')

def authenticate_google_drive():
    """Authenticate with Google Drive API using service account credentials from environment variables"""
    try:
        # Get credentials JSON from environment variable
        credentials_json = os.environ.get('GOOGLE_DRIVE_CREDENTIALS')
        
        if not credentials_json:
            logger.error("GOOGLE_DRIVE_CREDENTIALS environment variable not set")
            return None
        
        # Parse the JSON string to dictionary
        credentials_info = json.loads(credentials_json)
        
        # Define required scopes
        SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
        
        # Create credentials from the parsed JSON
        credentials = service_account.Credentials.from_service_account_info(
            credentials_info, scopes=SCOPES)
        
        drive_service = build('drive', 'v3', credentials=credentials)
        return drive_service
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        return None

def get_last_check_time():
    """Get the timestamp of the last folder check"""
    if os.path.exists(LAST_CHECK_FILE):
        with open(LAST_CHECK_FILE, 'r') as f:
            timestamp = f.read().strip()
            if timestamp:
                return timestamp
    
    # If no last check or file doesn't exist, return a time 24 hours ago
    # Use timezone-aware UTC datetime
    yesterday = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)).isoformat(timespec='seconds').replace('+00:00', 'Z')
    return yesterday

def update_last_check_time():
    """Update the timestamp of the last folder check"""
    now = datetime.datetime.now(datetime.timezone.utc).isoformat('T') + 'Z'
    with open(LAST_CHECK_FILE, 'w') as f:
        f.write(now)
    return now

def is_receipt_image(file):
    """Check if the file is likely a receipt image based on mime type"""
    mime_type = file.get('mimeType', '')
    return mime_type.startswith('image/')

def download_and_process_image(drive_service, file_id, file_name):
    """Download the image from Google Drive and save it to local directory"""
    try:
        # Get file metadata
        file_metadata = drive_service.files().get(
            fileId=file_id, 
            fields='size,name,createdTime,modifiedTime'
        ).execute()
        
        # Request file content
        request = drive_service.files().get_media(fileId=file_id)
        file_io = io.BytesIO()
        downloader = MediaIoBaseDownload(file_io, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
            logger.info(f"Download {int(status.progress() * 100)}%.")
        
        # Save to local file system
        file_path = os.path.join(IMAGE_DIR, file_name)
        with open(file_path, 'wb') as f:
            f.write(file_io.getvalue())
        
        # Print file information
        created_time = file_metadata.get('createdTime', 'N/A')
        modified_time = file_metadata.get('modifiedTime', 'N/A')
        size_bytes = int(file_metadata.get('size', 0))
        size_kb = size_bytes / 1024
        
        print(f"\nImage processed: {file_name}")
        print(f"Size: {size_kb:.2f} KB")
        print(f"Created: {created_time}")
        print(f"Last modified: {modified_time}")
        
        return file_path
    
    except Exception as e:
        logger.error(f"Error downloading file {file_id}: {str(e)}")
        return None

def check_for_new_images(folder_id):
    """Check for new images in the specified Google Drive folder"""
    drive_service = authenticate_google_drive()
    if not drive_service:
        logger.error("Failed to authenticate with Google Drive")
        return
    
    last_check_time = get_last_check_time()
    logger.info(f"Checking for images modified after {last_check_time}")
    
    try:
        # Query for files in the specified folder that are images and were created/moved to the folder after last check
        query = f"'{folder_id}' in parents and mimeType contains 'image/' and createdTime > '{last_check_time}'"
        #query = f"'{folder_id}' in parents"
        results = drive_service.files().list(
            q=query,
            spaces='drive',
            fields="files(id, name, mimeType, createdTime, modifiedTime, size)"
        ).execute()
        
        files = results.get('files', [])
        #print(files)  # Debugging line to see the files fetched
        
        if not files:
            logger.info("No new images found.")
            update_last_check_time()
            return
        
        logger.info(f"Found {len(files)} new images.")
        
        # Process each new image
        for file in files:
            file_id = file.get('id')
            file_name = file.get('name')
            
            logger.info(f"Processing image: {file_name}")
            download_and_process_image(drive_service, file_id, file_name)
        
        # Update the last check time
        update_last_check_time()
    
    except Exception as e:
        logger.error(f"Error checking for new images: {str(e)}")

def main():
    """Main function to run the daily monitoring process"""
    logger.info("Starting daily monitoring process")
    
    # Replace with your actual Google Drive folder ID where receipts are uploaded
    folder_id = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')
    if not folder_id:
        logger.error("GOOGLE_DRIVE_FOLDER_ID environment variable not set")
        return
    
    check_for_new_images(folder_id)
    
    logger.info("Daily monitoring process completed")

if __name__ == "__main__":
    main()