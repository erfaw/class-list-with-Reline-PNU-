### FULLY COPY FROM GOOGLE API DOCS QUICK START
from imports import *
from consts import *
import subprocess as sp; sp.call('cls', shell=True)

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    ## MAKE CALENDAR OBJECT AND CHECK FOR TOKEN CREDENTIALS
    calendar = GoogleCalendarManager()
    calendar.check_token()


    try:
        ## MAKE CALENDAR SERVICE, TO DO API CALLS THROUGH IT
        calendar.service = calendar.make_service_for_calendar()

        # Call FOR NEXT 10 EVENTS
        # calendar.get_and_print_upcoming_10_events()
        
        ## make a test event to learn.
        calendar.make_new_event(
            # TODO: check if this code need change or not (based on input from reline)
            start_time= datetime.time(7,0),
            end_time=datetime.time(8,0),
            title='salam',
            # start_date=datetime.date(year=2025,month=10,day=27),
            # end_date=datetime.date(year=2025,month=10,day=27),
            
        )
        input()

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
