# Smart Campus Lost-and-Found Assistant

A complete Python portfolio project that helps students report lost or found items, upload images, and discover possible matches.

## Why this project is resume-worthy

The project solves a clear real-world campus problem and demonstrates:

- Python programming
- Rule-based chatbot development
- Text processing
- Similarity matching
- SQLite database integration
- Image upload and file handling
- Streamlit web development
- Optional email notifications
- Admin dashboard development
- Automated testing

It remains simple enough to explain confidently in an interview.

## Features

- Chat-based lost-and-found assistant
- Detailed lost or found report form
- Item-image uploads
- Date, colour, location, and description fields
- SQLite report storage
- Weighted matching algorithm
- Match percentages
- On-screen match notifications
- Optional email alerts using SMTP
- Search page for existing reports
- Admin dashboard
- Resolve, reopen, and delete reports
- Automated tests

## How matching works

The project compares a new report with existing reports using a weighted score:

| Detail | Weight |
|---|---:|
| Item name | 45% |
| Colour | 15% |
| Location | 15% |
| Date | 10% |
| Description | 15% |

For example, a lost black wallet reported in the library can be matched with a found black wallet from the same location.

## Project structure

```text
smart_campus_lost_found_assistant/
├── app.py
├── seed_data.py
├── requirements.txt
├── .env.example
├── pages/
│   └── 1_Admin_Dashboard.py
├── src/
│   ├── chatbot.py
│   ├── database.py
│   ├── matcher.py
│   ├── notifications.py
│   ├── parser.py
│   └── storage.py
├── tests/
├── data/
└── uploads/
```

## Run in Windows PowerShell

```powershell
cd path\to\smart_campus_lost_found_assistant
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python seed_data.py
python -m streamlit run app.py
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

## Run in Command Prompt

```cmd
cd path\to\smart_campus_lost_found_assistant
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
python seed_data.py
python -m streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## Run tests

```bash
pytest -q
```

## Optional email setup

Email alerts are optional. The application works without them.

Copy `.env.example` to `.env`, add your SMTP details, and load those environment variables before starting the app.

For Gmail, use an App Password instead of your normal account password.

## Example chatbot messages

```text
I lost a black wallet in the library
I found a blue bottle in the cafeteria
Search for my silver keys
Show all reports
```

## Resume entry

**Smart Campus Lost-and-Found Assistant — Python, Streamlit, SQLite**

- Developed a Python chatbot that allows students to report lost and found items using natural-language messages and structured forms.
- Implemented keyword-based intent detection and automatic extraction of item, colour, and location information.
- Designed a weighted matching algorithm that compares item details, location, date, and description to generate match percentages.
- Integrated SQLite for report storage, image upload support, optional email notifications, and an admin dashboard for report management.
- Added automated tests for parsing, matching, and database operations.

## Interview explanation

> I built a Smart Campus Lost-and-Found Assistant using Python and Streamlit. A student can report an item through a chatbot or a form. The project stores the report in SQLite and compares it with existing reports using a weighted matching algorithm. The item name receives the highest weight, followed by colour, location, date, and description. When the score passes a threshold, the system shows a possible match and can optionally send an email alert. I also created an admin dashboard to resolve or delete reports.

## Main interview questions

### Why did you use SQLite?

SQLite is lightweight, requires no separate server, and is suitable for a small campus application or portfolio demonstration.

### Is this machine learning?

No. It uses transparent rule-based text processing and similarity scoring. This keeps the project reliable and easy to explain. Machine learning could be added later.

### How is the match percentage calculated?

Each item detail contributes a different percentage to the final score. Item name has the largest weight because it is the most important field.

### What would you improve next?

- Student login
- Better NLP with spaCy
- Image similarity
- Cloud database
- Real email notifications
- Mobile-friendly deployment
