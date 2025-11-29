from imports import *
from consts import *

class ChromeManager:
    def __init__(self):
        options = ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = Chrome(options= options)

        self.classes_df = None

    def format_converter(self, string):
        """catch a not formated string and replace letters with what we want. and return it"""
        return string.replace(r"/", '-').replace(r"،", ',').replace(r"۱",'1').replace(r"۲",'2').replace(r"۳",'3').replace(r"۴",'4').replace(r"۵",'5').replace(r"۶",'6').replace(r"۷",'7').replace(r"۸",'8').replace(r"۹",'9').replace(r"۹",'9').replace(r"۰",'0').replace(r")",')').replace(r"(",'(').replace(r"(",'(').replace(r"-",'-').replace(r"امتحان",'EXAM').replace(r"ساعت",'time').replace(r"درس(ت)", 'class').replace(r":", ':').replace("ي","ی").replace("ك", "ک").strip()
    
    def convert_persian_to_english_datestr(self, s):
        for fa, en in persian_weekdays.items():
            s = s.replace(fa, en)
        for fa, en in persian_months.items():
            s = s.replace(fa, en)
        return s
    
    def time_format(self, string):
        """use 'self.convert_persian_to_english_datestr()' and 'self.format_converter()' to return a acceptable format of datetime string."""
        return self.convert_persian_to_english_datestr(
            self.format_converter(
                string
                )
            )

    def switch_last_page(self):
        """swith driver focus to last exist tab in browser"""
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def login_reline(self, username, password,):
        """login to reline with user/pass in .env"""
        self.driver.get(f"{RELINE_URL}Identity/Account/Login?returnUrl=%2F")
        self.switch_last_page()
        ## WAIT TO LOAD LOGIN PAGE
        WebDriverWait(
            driver= self.driver,
            timeout= 30,
            poll_frequency= 1,
        ).until(
            EC.all_of(
                EC.element_to_be_clickable(
                    self.driver.find_element(By.ID, "Input_UserName")
                ),
                EC.element_to_be_clickable(
                    self.driver.find_element(By.ID, "password")
                ),
            )
        )

        ## FILL USERNAME and PASSWORD INPUT
        self.driver.find_element(By.ID, "Input_UserName").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        ## HIT 'VOROD' BTN
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, "button.btn").click()
        
        ## CHECK FOR LOGIN 
        self.switch_last_page()
        if WebDriverWait(
            driver= self.driver,
            timeout= 30,
            poll_frequency= 1,
        ).until(
            EC.title_is("داشبورد")
        ):
            print(f"LOGGED IN TO RELINE\nuser:\t<{username}>\n")

    def go_to_classes_part(self):
        self.driver.find_element(By.XPATH, "//a[contains(text(),'کلاس ها')]").click()
        ## CHECK FOR 
        self.switch_last_page()
        if WebDriverWait(
            driver= self.driver,
            timeout= 30,
            poll_frequency= 1,
        ).until(
            EC.title_is("کلاس")
        ):
            print(f"\nSWITCHED TO <classes list> PART\n")

    def scrape_to_classes_df(self):
        ## wait for load
        WebDriverWait(self.driver, 30, 1).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".card-body"))
            )

        ## CATCH ALL LESSONS FROM THIS SEMESTER
        all_this_term_classes_title = [tr for tr in self.driver.find_elements(By.CSS_SELECTOR, "div.card-body #table tbody tr") if tr.get_attribute("style") == '']

        ## CREATE PANDAS DATAFRAME FOR CLASSES
        self.classes_df = pd.DataFrame(
            data={},
            columns=["ID", "department", "semester", "lesson_name", "lesson_group_number", "sub-gp", "master", "class Type(distance/in-Person)", "link", "Fenglish"]
        )

        ## catch each part of table and record it to DF
        for lesson in all_this_term_classes_title:
            i=0
            lesson_ID = lesson.find_elements(By.CSS_SELECTOR, "td")[i].get_attribute('innerHTML')
            i+=1
            lesson_department = lesson.find_elements(By.CSS_SELECTOR, "td")[i].get_attribute('innerHTML').replace("دانشگاه پیام نور -", '')
            i+=1
            lesson_semester = lesson.find_elements(By.CSS_SELECTOR, "td")[i].get_attribute('innerHTML')
            i+=1
            lesson_lesson_name = lesson.find_elements(By.CSS_SELECTOR, "td")[i].get_attribute('innerHTML').split('(')[0]
            lesson_lesson_group_number = lesson.find_elements(By.CSS_SELECTOR, "td")[i].get_attribute('innerHTML').split('(')[1].replace(")",'')
            i+=1
            lesson_sub_gp = lesson.find_elements(By.CSS_SELECTOR, "td")[i].get_attribute('innerHTML')
            i+=1
            lesson_master = lesson.find_elements(By.CSS_SELECTOR, "td")[i].get_attribute('innerHTML')
            i+=1
            lesson_class_type = str(lesson.find_elements(By.CSS_SELECTOR, "td")[i].text)
            i+=1
            lesson_link = lesson.find_elements(By.CSS_SELECTOR, "td")[i].find_element(By.CSS_SELECTOR, "a").get_attribute('href')
            if Fenglish_class_names[self.format_converter(lesson_lesson_name).strip()]:
                lesson_fenglish_name = Fenglish_class_names[self.format_converter(lesson_lesson_name).strip()]
            else: 
                lesson_fenglish_name = input(f"Insert Fenglish string for this lesson, <{self.format_converter(lesson_lesson_name)}>,\nCareful:\tthis gonna used to make events titles in Google Calendar!!\n>> ")

            ##fill record to df
            self.classes_df.loc[len(self.classes_df)] = {
                "ID":lesson_ID,
                "department":self.format_converter(lesson_department),
                "semester":self.format_converter(lesson_semester),
                "lesson_name":self.format_converter(lesson_lesson_name),
                "lesson_group_number":self.format_converter(lesson_lesson_group_number),
                "sub-gp":self.format_converter(lesson_sub_gp),
                "master":self.format_converter(lesson_master),
                "class Type(distance/in-Person)":self.format_converter(lesson_class_type),
                "link":lesson_link,
                "Fenglish": lesson_fenglish_name,
            }
            print()
        
        print("\nALL CLASSES SCRAPED TO DATAFRAME!! \n")