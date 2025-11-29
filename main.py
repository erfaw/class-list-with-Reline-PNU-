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
## TODO : make a notification for when the excel file is open and we have access denied from OS
chrome.classes_df.to_excel(excel_fp,"all_classes")

## LOOP THROUGH CLASSES_DF FOR EVERY LINK IS IN IT,
for i, clss in chrome.classes_df.iterrows():
    ## GET TO PAGE 
    chrome.driver.get(clss.link)
    time.sleep(3)

    ## GET ALL OF ROWS FROM SESSIONS 
    all_sessions = chrome.driver.find_element(By.CSS_SELECTOR, ".table").find_elements(By.CSS_SELECTOR, "tr")
    ## make DF for classes times table
    sessions_df = pd.DataFrame(
        data={},
        columns=["start", "end"]
    )

    ## LOOP THROUGH EACH SESSION AND FILL A DATAFRAME AND SHEET FOR IT WITH END AND START TIME AND DATE IN EXCEL FILE
    is_first_round = True
    for session in all_sessions:
        ## IF IS FIRST PASS, (BECAUSE ITS HEADER OF TABLE)
        if is_first_round:
            is_first_round = False
            continue

        ### CATCH START AND END TIME FROM THAT ROW OF TABLE
        ## 1.START >
        #MAKE START_TIME EN TYPED
        start_time = chrome.convert_persian_to_english_datestr(
            chrome.format_converter(
                session.find_elements(By.CSS_SELECTOR, "td")[2].text
                )
            )

                # TODO : somehow 1. convert this format to en format, 2. somehow convert persian calendar to christian calendar
                # if len(start_time.split()) != 6 or len(start_time.split()) > 6:
                    # TODO : figure it out how get object from these code, (i curious about chrome.format_converter, we must try one time without it)
                    ### tarkibe barande :
                                # format_string= r'%A %d %B %Y - %H:%M'
                                # x=jdatetime.datetime.strptime(end_, format_string,)
                            # first_part = "".join(start_time.split()[0:2])
                            # second_part = start_time.split()[2:]
                            # end_ = [first_part]
                            # start_time = end_.extend(second_part)

        #MAKE DATETIME OBJ IN PERSIAN CALENDAR
        format_new = r'%A %d %B %Y - %H:%M'
        start_time = jdatetime.datetime.strptime(start_time, format_new)

        ## 2.END_TIME >
        #MAKE END_TIME EN TYPED
        end_time = chrome.convert_persian_to_english_datestr(
            chrome.format_converter(
                session.find_elements(By.CSS_SELECTOR, "td")[3].text
                )
            )
        #MAKE DATETIME OBJ IN PERSIAN CALENDAR
        format_new = r'%A %d %B %Y - %H:%M'
        end_time = jdatetime.datetime.strptime(end_time, format_new)

        ## MAKE A RECORD ON DATAFRAME
        sessions_df.loc[len(sessions_df)] = {
            "start": start_time,
            "end": end_time
        }


    ## MAKE INDEXES OF DATAFRAME BEGIN WITH 1
    sessions_df.index=pd.RangeIndex(1,len(sessions_df)+1)

    # TODO: catch 'Permision Denied OS' and exit file which is open right now
    ## WRITE DATAFRAME IN A SHEET WITH OWN SHEET_NAME IN EXCEL FILE
    with pd.ExcelWriter(excel_fp, mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
        sessions_df.to_excel(
            writer,
            sheet_name=f"{clss["lesson_name"]}",
            # startrow= 1
        )
    # TODO: make a notification for 'end of procedure'
    print()

## make a test event to learn.
        # calendar.make_new_event(
        #     # TODO: check if this code need change or not (based on input from reline)
        #     start_time= datetime.time(7,0),
        #     end_time=datetime.time(8,0),
        #     title='salam',
        #     # start_date=datetime.date(year=2025,month=10,day=27),
        #     # end_date=datetime.date(year=2025,month=10,day=27),
            
        # )