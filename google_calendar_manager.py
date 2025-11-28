from imports import *
from consts import *

class GoogleCalendarManager:
    def __init__(self):
        self.creds = None 
        self.service = None
    
    def check_token(self):
        """checking existion of 'token.json' and credentials"""
        ## IF 'TOKEN.JSON' EXIST, LOAD IT IN SELF.CREDS
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        ## IF THERE ARE NO (VALID) CREDENTIALS AVAILABLE, LET THE USER LOG IN.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())     

    def make_service_for_calendar(self):
        return build("calendar", "v3", credentials=self.creds)
    
    