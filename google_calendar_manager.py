from imports import *
from consts import *

class GoogleCalendarManager:
    def __init__(self):
        # self.remove_url = "https://www.googleapis.com/calendar/v3/calendars/primary/events/"
        self.creds = None 
        self.service = None
        # self.events = None
        self.BASE_CALENDAR_NAME = "BOT-ADDED CLASSES"
        self.BASE_CALENDAR_ID = None
        self.iran_tz = pytz.timezone('Asia/Tehran') 
        self.check_token()
        ## MAKE CALENDAR SERVICE, TO DO API CALLS THROUGH IT
        self.service = self.make_service_for_calendar()
        self.calendar_ids:dict = self.get_list_of_user_calendars()
    
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
    
    def get_and_print_upcoming_10_events(self, calendar_id):
        """api call to 'Google Calendar API' and print next 10 events (if exists)"""
        ## GET CURRENT DATE TIME
        now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

        ## PRINT MESSAGE IN CONSOLE
        print("Getting the upcoming 10 events")

        ## MAKE API CALL AND GET 10 UPCOMING EVENTS AND STORE IT
        events_result = (
            self.service.events()
            .list(
                calendarId= calendar_id,
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

    def make_new_calendar(self, _calednar_name) -> json:
        """makes a new calendar and pass calendar id"""
        body_calendar = {
            'summary': _calednar_name,
            'timeZone': f"{self.iran_tz}",
        }
        response = self.service.calendars().insert(body=body_calendar).execute()
        print(f"NEW CALENDAR INITIALIZED <{response['summary']}>")
        return response
        #TODO: check it.
    
    def delete_sec_calendar(self, _calendar_id):
        """permenantly delete a second calendar with given calendarId"""
        self.service.calendars().delete(
            calendarId= _calendar_id
            ).execute()
        print(f"PREV-CALENDAR DELETED!")
        
    def clear_sec_calendar(self, _calendar_id):
        """clear an existing calendar with given calendarId"""
        ## TODO: check it .
        self.service.calendars().clear(
            calendarId= _calendar_id
            ).execute()

    def get_list_of_user_calendars(self) -> list:
        """api call and get current user calendars list with data from each."""
        response = self.service.calendarList().list().execute()
        return response['items']

    def make_new_event(
        self,
        # NON-DEFAULT VALUES ==>
        calendar_id:str,
        title:str,
        start_time:datetime.time,
        end_time :datetime.time,
        # DEFAULT VALUES ==>
        end_date:datetime.date= datetime.date.today(),
        start_date:datetime.date= datetime.date.today(),
        description:str= '',
        location= None,
        color_id:int= EVENT_COLOR_ID["tangerine"],
        ) -> json:
        """make a Event in user Google Calendar and fill it with given arg details. then, return event creation response"""
        ## MAKE A DATETIME WIHT ISO FORMAT (AND BRING BACK 4 MINUTES TO FIT WITH REAL WORLD)
        start_date_time = (datetime.datetime.combine(
            start_date, start_time, self.iran_tz
        )-timedelta(minutes=4)).isoformat()

        end_date_time = (datetime.datetime.combine(
            end_date, end_time, self.iran_tz
        )-timedelta(minutes=4)).isoformat()

        ## MAKE EVENT DETAILS IN A DICTIONARY TO PASS TO API
        event = { #notice: this is a boilerplate of Event Resources of a EVENT that must be like this, DONT REMOVE ANY PART OF IT.
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
                    {'method': 'popup', 'minutes': 60*24*1},
                ],
            },
            ## SET COLOR OF EVENT (MUST BE RED FOR CLASSES)
            "colorId": color_id,
        }

        ## CALL API AND MAKE EVENT ON USER PRIMARLY CALENDAR 
        response = self.service.events().insert(
            calendarId= calendar_id,
            body= event
        ).execute()
        # TODO: ADD EVENT TITLE TO BELOW PRINT STATEMENT for adding event
        print(f'EVENT CREATED')
        return response
    
    def remove_event(self, _id, calendar_id):
        """remove a event with its id"""
        try:
            self.service.events().delete(
                calendarId= calendar_id,
                eventId= _id,
            ).execute()
        except HttpError as e: 
            # TODO: good to be just e.message
            print(e)
        else:
            # TODO: ADD EVENT TITLE TO BELOW PRINT STATEMENT for removing event
            print("EVENT DELETED!!")

    def remove_previous_calendar_and_replace_new(self) -> str:
        """remove base calendar and build it from scratch"""
        for calendar in self.calendar_ids:
            if calendar['summary'] == self.BASE_CALENDAR_NAME:
                result = calendar['id']
                break
            else: 
                result = False
        
        if result:
            self.delete_sec_calendar(result)

        response = self.make_new_calendar(self.BASE_CALENDAR_NAME)
        return response['id']