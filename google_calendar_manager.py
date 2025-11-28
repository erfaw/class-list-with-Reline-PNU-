from imports import *
from consts import *

class GoogleCalendarManager:
    def __init__(self):
        self.creds = None 
        self.service = None
    
    def check_token(self):
        """checking existion of 'token.json' and credentials. THE FILE TOKEN.JSON STORES THE USER'S ACCESS AND REFRESH TOKENS, AND IS CREATED AUTOMATICALLY WHEN THE AUTHORIZATION FLOW COMPLETES FOR THE FIRST TIME."""
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
        """build a service from 'Google Calendar' to make api calls and manipulate calendar for user."""
        return build("calendar", "v3", credentials=self.creds)
    
    def get_and_print_upcoming_10_events(self):
        """api call to 'Google Calendar API' and print next 10 events (if exists)"""
        ## GET CURRENT DATE TIME
        now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

        ## PRINT MESSAGE IN CONSOLE
        print("Getting the upcoming 10 events")

        ## MAKE API CALL AND GET 10 UPCOMING EVENTS AND STORE IT
        events_result = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )  
        events = events_result.get("items", []) 

        ## CHECKING: THERE IS ANY EVENTS TO SHOW OR NOT
        if not events:
            print("No upcoming events found.")
            return

        ## PRINTS THE START AND NAME OF THE NEXT 10 EVENTS
        index = 1
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(f"\n{index}. Time: <{start}>\n\tsummary: <{event["summary"]}>")
            index += 1

        print("\nEND OF EVENTS!!")     