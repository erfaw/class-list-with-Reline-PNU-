### 1. built-ins
import datetime
from datetime import timedelta
import os.path
import pytz
import time
import json
import requests

### 2. third parties
#google calendar api
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
#selenium
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
#dotenv
from dotenv import load_dotenv
#pandas
import pandas as pd
from pathlib import Path
#jdatetime
import jdatetime
#plyer
from plyer import notification

### 3. self made
from google_calendar_manager import GoogleCalendarManager
from chrome_manager import ChromeManager
from consts import *