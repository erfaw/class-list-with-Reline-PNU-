from imports import *
from consts import *

class ChromeManager:
    def __init__(self):
        options = ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = Chrome(options= options)

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
        WebDriverWait(
            driver= self.driver,
            timeout= 30,
            poll_frequency= 1,
        ).until(
            EC.title_is("داشبورد")
        )
        print(f"LOGGED IN TO RELINE\nuser:\t<{username}>")