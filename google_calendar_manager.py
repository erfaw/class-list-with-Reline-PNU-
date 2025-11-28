from imports import *
from consts import *

class GoogleCalendarManager:
    def __init__(self):
        self.creds = None 
        self.service = None
        self.events = None
        self.iran_tz = pytz.timezone('Asia/Tehran') 
        self.check_token()
        ## MAKE CALENDAR SERVICE, TO DO API CALLS THROUGH IT
        self.service = self.make_service_for_calendar()
    
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

    def make_new_event(
        self,
        title:str,
        start_time:datetime.time,
        end_time :datetime.time,
        end_date:datetime.date=datetime.date.today(),
        start_date:datetime.date=datetime.date.today(),
        description:str='',
        location= None,
        color_id:int= EVENT_COLOR_ID["tomato"]
        ):
        """make a Event in user Google Calendar and fill it with given arg details."""
        ## MAKE A DATETIME WIHT ISO FORMAT (AND BRING BACK 4 MINUTES TO FIT WITH REAL WORLD)
        start_date_time = (datetime.datetime.combine(
            start_date, start_time, self.iran_tz
        )-timedelta(minutes=4)).isoformat()
        end_date_time = (datetime.datetime.combine(
            end_date, end_time, self.iran_tz
        )-timedelta(minutes=4)).isoformat()

        ## MAKE EVENT DETAILS IN A DICTIONARY TO PASS TO API
        event = {
            'summary': title,
            'location': None,
            'description': description,
            'start': {
                'dateTime': f'{start_date_time}',
                'timeZone': f'{self.iran_tz}',
            },
            'end': {
                'dateTime': f'{end_date_time}',
                'timeZone': f'{self.iran_tz}',
            },
            ## COMMENTED OUT 'REPEAT' AND 'COMPANY' FUNCITONS FOR EACH EVENT
            # 'recurrence': [
            #     'RRULE:FREQ=DAILY;COUNT=2'
            # ],
            # 'attendees': [
            #     {'email': 'lpage@example.com'},
            #     {'email': 'sbrin@example.com'},
            # ],
            ## SET 1MINUTE, 15MINUTE, 4WEEK REMINDER
            'reminders': {
                'useDefault': False,
                'overrides': [
                {'method': 'popup', 'minutes': 15},
                {'method': 'popup', 'minutes': 1},
                {'method': 'popup', 'minutes': 60*24*30},
                ],
            },
            ## SET COLOR OF EVENT (MUST BE RED FOR CLASSES)
            "colorId": color_id,
        }

        ## CALL API AND MAKE EVENT ON USER PRIMARLY CALENDAR 
        self.service.events().insert(
            calendarId= 'primary',
            body= event
        ).execute()
        print('EVENT CREATED')