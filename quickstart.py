### FULLY COPY FROM GOOGLE API DOCS QUICK START
from imports import *
from consts import *

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

        # Call the Calendar API
        calendar.get_and_print_upcoming_10_events()

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
