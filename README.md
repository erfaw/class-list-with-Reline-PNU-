

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
