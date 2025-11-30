def exit_on_dependency_error(package_name, install_command):
    """Prints a clear error message and exits the program."""
    print("\n" + "="*70)
    print(f"FATAL ERROR: Required dependency '{package_name}' is not installed.")
    print("Please install it using the following command:")
    print(f"\n   >>> {install_command}")
    print("="*70 + "\n")
    sys.exit(1)

### 1. built-ins
import datetime
from datetime import timedelta
import os.path
import time
import json
import requests
import sys
from pathlib import Path

### 2. third parties
#google calendar api
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    exit_on_dependency_error("Google API Libraries", "pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")

#selenium
try:
    from selenium.webdriver import Chrome
    from selenium.webdriver import ChromeOptions
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
except ImportError:
    exit_on_dependency_error("Selenium", "pip install selenium")

#dotenv
try:
    from dotenv import load_dotenv
except ImportError:
    exit_on_dependency_error("python-dotenv", "pip install python-dotenv")

#pandas
try:
    import pandas as pd
except ImportError:
    exit_on_dependency_error("pandas", "pip install pandas")

#jdatetime
try:
    import jdatetime
except ImportError:
    exit_on_dependency_error("jdatetime", "pip install jdatetime")

# pytz (Needed for timezone awareness, even though it's often a dependency of others)
try:
    import pytz
except ImportError:
    exit_on_dependency_error("pytz", "pip install pytz")

# plyer
try:
    from plyer import notification
except ImportError:
    exit_on_dependency_error("plyer", "pip install plyer")

### 3. self made
from google_calendar_manager import GoogleCalendarManager
from chrome_manager import ChromeManager
from consts import *

## TODO: GOOD TO BE KIND OF CODE HERE: TO CHECK WITH ALL 'requirements.txt': if user had it: skip, if user didn't had it: pip install for it