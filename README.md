<!-- TODO: ADD EXPLANATION FOR 1. WHAT IS RELINE, 2. THIS PROJECT HADNY FOR WHAT KIND OF STUDENTS, 3. THIS PROJECT WHAT DO RIGHT NOW, 4. ADDING PICTURE AND GIFS FOR EACH SESSION IF NEEDED, -->
-----------------------------------
# What This Program Does Exactly?

This application is designed for students who want to seamlessly integrate their academic life with their digital planning tools. 
## Could work for you If you are:
- A PNU (Payame Noor University) student needing to manage course schedules.
- Someone who habitually uses [Google Calendar](https://calendar.google.com/) to organize tasks, set reminders, and track events.
This program automates the process of fetching and adding your PNU-related events (for now just Class Dates) directly into your Google Calendar, ensuring you never miss. It acts as the bridge between your university schedule and your personal digital organizer.

-----------------------------------------

## How ?

### ✅ 1. Clone this project:
```
git clone https://github.com/erfaw/class-list-with-Reline-PNU-
```


### ✅ 2. Install dependencies
```
pip install -r requirements.txt
```



### ✅ 3. make a `.env` file next to `main.py`:

```
New-Item .env -ItemType File
```



### ✅ 4. Fill your `USERNAME_RELINE` and `PASSWORD_RELINE` of [RELINE](https://lms.pnu.ac.ir/) profile like this:
```
USERNAME_RELINE="your-username-must-be-here"
PASSWORD_RELINE="your-password-must-be-here"
```

Note: dont share this `.env` to others!



### ✅ 5. Create your Google API credentials and get `credential.json`
This project uses the Google Calendar API, which requires OAuth credentials.
Because of security reasons, the file `credentials.json` is **NOT included** in the repository.
Each user must create their own credentials.
Follow these steps:

1) Go to [Google Cloud Console](https://console.cloud.google.com/)

2) Create a new project (or use an existing one)

3) Enable the Google Calendar API
APIs & Services → Library → Google Calendar API → Enable

4) Go to:
APIs & Services → Credentials → Create Credentials → OAuth Client ID

5) Choose:

* Application type: Desktop Application

* Name: anything you want

NOTE: You have to choose `https://www.googleapis.com/auth/calendar` in 'scope' part, to program work currectly

6) Click “Create” and download the file:
`credentials.json`

NOTE: if file name was different: change it to `credentials.json`

7) Put the file in the root directory of this project, like this:
```
project/
    main.py
    credentials.json
    token.json (auto-created after first run)
```
NOTE: dont share this `credential.json` to others!



### ✅ 6. First run

Start the program:
```
python main.py
```

The browser will open and ask you to log into Google.
After authorization, a file named `token.json` will be created automatically.

This file stores the refreshed tokens so you won’t need to authorize every time.

--------------------------------------------------

## 📌 Notes

Never commit `credentials.json` or `token.json` to Git.

These files are already in `.gitignore.`

If you need to distribute the app, each user **must create their own credentials** (this is required by Google for security reasons).

-------------------------------

## 🛡 Security Reminder

``credentials.json`` contains your client ID and client secret.
Treat it like a password.
Do NOT upload it to GitHub, even in private repos.

---------------------------
---------------------------
--------------------------

# What is [PNU](https://pnu.ac.ir/en-US/DouranPortal/7293/page/Payame-Noor-University) ?!
The acronym PNU refers to Payame Noor University, which is a major distance learning and open university system in Iran. 🎓

# What is [RELINE](https://lms.pnu.ac.ir/) ?!
RELINE is a Learning Management System (LMS) used by Payame Noor University (PNU). Its primary function is to host and deliver the university's non-attendance and distance education courses online. RELINE facilitates all aspects of the virtual learning process, including providing access to digital course materials (Often), holding virtual classes and meetings, and managing online assignments and exams for PNU students (Like me 😉)

