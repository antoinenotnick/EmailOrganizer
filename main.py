from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os

# Define the scopes for Gmail API
SCOPES = ['https://mail.google.com/']


def authenticate():
    creds = None

    # Check if token.pickle file exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials are available, prompt the user to authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Create OAuth 2.0 flow using the client secrets file
            flow = InstalledAppFlow.from_client_secrets_file(
                r'C:\Users\antho\OneDrive\Documents\VS_Code\GmailOrganizer\client_secret_321183515633-oq3n3rv1mi6rdj7s1mgq0ko1vopji310.apps.googleusercontent.com.json', scopes=SCOPES)
            
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    if not creds:
        raise Exception('Failed to authenticate')
    
    return creds

def fetch_emails(service, query=''):
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    return messages

def delete_email(service, email_id):
    try:
        service.users().messages().delete(userId='me', id=email_id).execute()
        print(f'Email with ID {email_id} deleted successfully.')
    
    except Exception as e:
        print(f'An error occurred while deleting email with ID {email_id}: {e}')

def main():
    try:
        # Authenticate and get the Gmail API service
        creds = authenticate()
        service = build('gmail', 'v1', credentials=creds)

        while True:
            try:
                # Fetch emails with a specific query
                emails = fetch_emails(service, query= 'from:no-reply@duolingo.com')          #input('from:'))

                # Print email IDs and delete emails
                for email in emails:
                    print(email['id'])
                    delete_email(service, email['id'])
            except KeyboardInterrupt:
                continue

    
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()

