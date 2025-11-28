from imports import *
from consts import *
import subprocess as sp; sp.call('cls', shell=True)
current_dir = Path(__file__).parent.resolve()
load_dotenv()

## MAKE CALENDAR and CHROME DRIVER OBJECT
chrome = ChromeManager()
calendar = GoogleCalendarManager()

## LOGGING IN TO 'RELINE_URL'
chrome.login_reline(username=os.environ.get('USERNAME_RELINE'), password= os.environ.get("PASSWORD_RELINE"))

## GO TO CLASSES PART
chrome.go_to_classes_part()

chrome.scrape_to_classes_df()
    

#sotre pandas df to see
excel_fp_dir = current_dir/'output'
excel_fp_dir.mkdir(exist_ok=True)
excel_fp = excel_fp_dir/'result.xlsx'
chrome.classes_df.index= pd.RangeIndex(1, len(chrome.classes_df)+1)
chrome.classes_df.to_excel(excel_fp,"all_classes")


input()
## make a test event to learn.
        # calendar.make_new_event(
        #     # TODO: check if this code need change or not (based on input from reline)
        #     start_time= datetime.time(7,0),
        #     end_time=datetime.time(8,0),
        #     title='salam',
        #     # start_date=datetime.date(year=2025,month=10,day=27),
        #     # end_date=datetime.date(year=2025,month=10,day=27),
            
        # )