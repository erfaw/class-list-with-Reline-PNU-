from imports import *
from consts import *
import subprocess as sp; sp.call('cls', shell=True)
current_dir = Path(__file__).parent.resolve()
load_dotenv()

## TODO: MAKE A 'DATAMANAGER.PY' FILE AND MOVE DATA STORING AND DATA PROCESSING IN IT

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
        columns=["start_persian", "end_persian", "start_christian", "end_christian", "event_id", "event_link", "event_iCalUID"]
    )

    ## LOOP THROUGH EACH SESSION AND FILL A DATAFRAME AND SHEET FOR IT WITH END AND START TIME AND DATE IN EXCEL FILE
    session_index = 1
    is_first_round = True
    for session in all_sessions:
        ## IF IS FIRST PASS, (BECAUSE ITS HEADER OF TABLE)
        if is_first_round:
            is_first_round = False
            continue

        ### CATCH START AND END TIME FROM THAT ROW OF TABLE
        ## 1.START >
        #MAKE START_TIME EN TYPED
        start_time_bad_format = session.find_elements(By.CSS_SELECTOR, "td")[2].text
        start_time = chrome.time_format(start_time_bad_format)
        #MAKE DATETIME OBJ IN PERSIAN CALENDAR
        start_time = jdatetime.datetime.strptime(
            date_string= start_time,
            format= r'%A %d %B %Y - %H:%M'
            )
        ## 2.END_TIME >
        #MAKE END_TIME EN TYPED
        end_time_bad_format = session.find_elements(By.CSS_SELECTOR, "td")[3].text
        end_time = chrome.time_format(end_time_bad_format)
        #MAKE DATETIME OBJ IN PERSIAN CALENDAR
        end_time = jdatetime.datetime.strptime(
            date_string= end_time,
            format= r'%A %d %B %Y - %H:%M'
            )

        ## MAKE A EVENT FOR EACH SESSION IN GOOGLE CALENDAR
        event_response = calendar.make_new_event(
            title= f"Class: ({session_index}/{len(all_sessions)}) {clss["Fenglish"]}",
            start_time= start_time.time(),
            end_time= end_time.time(),
            start_date= start_time.togregorian().date(),
            end_date= end_time.togregorian().date(),
            # TODO: make description clean
            description= f"----------\nID=<{clss['ID']}>,\ndepartment=<{clss['department']}>\nsemester=<{clss['semester']}>\nGroup Num.=<{clss['lesson_group_number']}-{clss['sub-gp']}>\nclass type=<{clss['class Type(distance/in-Person)']}>\nLINK-Reline=<{clss['link']}>\n----------"
        )

        ## MAKE A RECORD ON DATAFRAME (all in iso format)
        sessions_df.loc[len(sessions_df)] = {
            "start_persian": start_time.isoformat(),
            "end_persian": end_time.isoformat(),
            "start_christian":start_time.togregorian().isoformat(),
            "end_christian":end_time.togregorian().isoformat(),
            "event_id":event_response['id'],
            "event_link":event_response['htmlLink'],
            "event_iCalUID":event_response['iCalUID'],
        }
        session_index += 1

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
    
print("\nALL CLASSES AND SESSIONS INSERTED TO EXCEL FILE WITH GREGORIAN FORMAT DATE !!")