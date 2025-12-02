<!-- TODO: ADD EXPLANATION FOR 1. WHAT IS RELINE, 2. THIS PROJECT HADNY FOR WHAT KIND OF STUDENTS, 3. THIS PROJECT WHAT DO RIGHT NOW, 4. ADDING PICTURE AND GIFS FOR EACH SESSION IF NEEDED, -->
-----------------------------------
# What This Program Does Exactly?

This application is designed for students who want to seamlessly integrate their academic life with their digital planning tools. 
## If you are:
- A PNU (Payame Noor University) student needing to manage course schedules.
- Someone who habitually uses [Google Calendar](https://calendar.google.com/) to organize tasks, set reminders, and track events.
This program automates the process of fetching and adding your PNU-related events (for now just Class Dates) directly into your Google Calendar, ensuring you never miss. It acts as the bridge between your university schedule and your personal digital organizer.
## How ?
1. Clone this project:
```
git clone https://github.com/erfaw/class-list-with-Reline-PNU-
```

2. make a `.env` file next to `main.py`:

```
New-Item .env -ItemType File
```

3. Fill your `USERNAME_RELINE` and `PASSWORD_RELINE` of [RELINE](https://lms.pnu.ac.ir/) profile like this:
```
USERNAME_RELINE='your-username-must-be-here'
PASSWORD_RELINE='your-password-must-be-here'
```

Note: dont share this `.env` to others!

4. Go to [Project Setup – Google Calendar API (Python)](https://github.com/erfaw/class-list-with-Reline-PNU-/blob/main/README.md#project-setup--google-calendar-api-python) and follow procedure to get `credential.json`

5. Copy-Paste `credential.json` next to `main.py`
   
NOTE: dont share this `credential.json` to others!

6. 

# What is [PNU](https://pnu.ac.ir/en-US/DouranPortal/7293/page/Payame-Noor-University) ?!
The acronym PNU refers to Payame Noor University, which is a major distance learning and open university system in Iran. 🎓

# What is [RELINE](https://lms.pnu.ac.ir/) ?!
RELINE is a Learning Management System (LMS) used by Payame Noor University (PNU). Its primary function is to host and deliver the university's non-attendance and distance education courses online. RELINE facilitates all aspects of the virtual learning process, including providing access to digital course materials (Often), holding virtual classes and meetings, and managing online assignments and exams for PNU students (Like me 😉)

-----------------------------------

# Project Setup – Google Calendar API (Python)

This project uses the Google Calendar API, which requires OAuth credentials.
Because of security reasons, the file `credentials.json` is **NOT included** in the repository.
Each user must create their own credentials.

## ✅ 1. Install dependencies
```
pip install -r requirements.txt
```
----------------------
## ✅ 2. Create your Google API credentials

### Follow these steps:

Go to [Google Cloud Console](https://console.cloud.google.com/)

Create a new project (or use an existing one)

Enable the Google Calendar API
APIs & Services → Library → Google Calendar API → Enable

Go to:
APIs & Services → Credentials → Create Credentials → OAuth Client ID

Choose:

* Application type: Desktop Application

* Name: anything you want

Click “Create” and download the file:
`credentials.json`

Put the file in the root directory of this project, like this:
```
project/
    main.py
    credentials.json
    token.json (auto-created after first run)
```
-----------------------
## ✅ 3. First run

Start the program:
```
python main.py
```

The browser will open and ask you to log into Google.
After authorization, a file named `token.json` will be created automatically.

This file stores the refreshed tokens so you won’t need to authorize every time.

------------------------

## 📌 Notes

Never commit `credentials.json` or `token.json` to Git.

These files are already in `.gitignore.`

If you need to distribute the app, each user **must create their own credentials** (this is required by Google for security reasons).

-------------------------------

## 🛡 Security Reminder

``credentials.json`` contains your client ID and client secret.
Treat it like a password.
Do NOT upload it to GitHub, even in private repos.
