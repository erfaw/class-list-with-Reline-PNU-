from imports import *
from consts import *
import subprocess as sp; sp.call('cls', shell=True)

## MAKE CALENDAR OBJECT
calendar = GoogleCalendarManager()



## make a test event to learn.
        # calendar.make_new_event(
        #     # TODO: check if this code need change or not (based on input from reline)
        #     start_time= datetime.time(7,0),
        #     end_time=datetime.time(8,0),
        #     title='salam',
        #     # start_date=datetime.date(year=2025,month=10,day=27),
        #     # end_date=datetime.date(year=2025,month=10,day=27),
            
        # )