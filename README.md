# EduSmart AI – Intelligent Student Learning and Academic Management System

[![Python Version](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask%203.0-green.svg)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20SQLAlchemy-orange.svg)](https://www.sqlite.org/)
[![UI Style](https://img.shields.io/badge/UI-Bootstrap%205%20%2B%20Chart.js-purple.svg)](https://getbootstrap.com/)
[![AI Provider](https://img.shields.io/badge/AI-Google%20Gemini-red.svg)](https://ai.google.dev/)

---

## 1. Project Overview

**EduSmart AI** is a complete, production-grade, university-level web application designed to solve the problem of fragmented student productivity tools. It centralizes course management, schedule planning, digital lecture notes, assignment tracking, active recall self-assessment, and conversational AI tutoring into a single cohesive platform.

Developed as an individual Undergraduate CSE Capstone Project, EduSmart AI enforces clean software design patterns (Application Factory, MVC, Blueprints, ORM, Role-Based Access Control) with zero external commercial dependencies.

---

## 2. Technology Stack

* **Backend:** Python 3.11+, Flask 3.0.3, Werkzeug (Password Hashing & Security)
* **ORM & Database:** Flask-SQLAlchemy 3.1.1, SQLite 3 (12 Normalized Relational Tables)
* **Frontend:** HTML5, CSS3, JavaScript (ES6), Bootstrap 5.3, Bootstrap Icons, Chart.js 4.4
* **AI Engine:** Google Gemini Generative AI API (`google-generativeai` / `google-genai`)
* **Environment & Security:** `python-dotenv`, CSRF/XSS protection, Session Management, RBAC

---

## 3. Directory Structure

```
edusmart-ai/
│
├── app.py                      # Main entry point and database seeder
├── config.py                   # Centralized environment configuration
├── requirements.txt            # Python dependencies
├── .env.example                # Template for environment secrets
├── .env                        # Local environment variables (API keys, secret key)
├── .gitignore                  # Git exclusions (venv, instance db, uploads)
│
├── app/
│   ├── __init__.py             # Flask Application Factory (create_app)
│   ├── extensions.py           # SQLAlchemy extension initialization
│   │
│   ├── models/                 # 12 Relational SQLAlchemy models
│   │   ├── __init__.py         # Model package registry
│   │   ├── user.py             # User model (Student & Admin roles, hashing)
│   │   ├── subject.py          # Enrolled academic subjects
│   │   ├── task.py             # Study planner scheduled tasks
│   │   ├── note.py             # Digital lecture notes & uploaded PDF files
│   │   ├── quiz.py             # AI Quizzes, Questions, and Attempt scores
│   │   ├── assignment.py       # Coursework assignments & deadline alerts
│   │   ├── notification.py     # In-app notifications
│   │   ├── study_session.py    # Time logging for analytics
│   │   └── activity_log.py     # Platform audit trail
│   │
│   ├── routes/                 # Modular Flask Blueprints
│   │   ├── auth.py             # Register, Login, Logout, Profile settings
│   │   ├── dashboard.py        # KPIs, subjects, study hours log, notifications
│   │   ├── planner.py          # Daily/weekly study planner & status toggling
│   │   ├── notes.py            # Notes CRUD, search, and PDF attachments
│   │   ├── quiz.py             # AI quiz generation, test taking & auto-grading
│   │   ├── assistant.py        # Conversational AI study assistant (AJAX)
│   │   ├── assignments.py      # Assignment manager with deadline filters
│   │   └── admin.py            # Administrative panel & audit log observer
│   │
│   ├── services/               # Business logic separation
│   │   ├── ai_service.py       # Google Gemini LLM API integration
│   │   └── analytics_service.py# Chart.js statistics & metric aggregators
│   │
│   ├── templates/              # Jinja2 HTML5 Templates
│   │   ├── base.html           # Master layout with responsive sidebar & topbar
│   │   ├── landing.html        # Public marketing & feature overview
│   │   ├── auth/               # login.html, register.html, profile.html
│   │   ├── dashboard/          # index.html, subjects.html, notifications.html
│   │   ├── planner/            # index.html (study task schedule)
│   │   ├── notes/              # index.html, create.html, view.html, edit.html
│   │   ├── quiz/               # index.html, take.html, result.html
│   │   ├── assistant/          # index.html (conversational chat)
│   │   ├── assignments/        # index.html (coursework tracker)
│   │   ├── admin/              # index.html (system oversight)
│   │   └── errors/             # 403.html, 404.html, 500.html
│   │
│   └── static/
│       ├── css/style.css       # Custom SaaS design styling and color variables
│       └── js/main.js          # Auto-dismiss alerts, tooltips, DOM interactions
│
├── instance/
│   └── edusmart.db             # SQLite database (auto-generated)
├── uploads/                    # Secure local storage for uploaded PDF notes
└── tests/
    └── test_app.py             # Automated unit & integration test suite
```

---

## 4. Installation & Setup Guide

### Step 1: Open Terminal in the Project Directory
```powershell
cd C:\Users\tasni\.gemini\antigravity\scratch\edusmart-ai
```

### Step 2: Activate Virtual Environment
```powershell
.\venv\Scripts\activate
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Copy `.env.example` to `.env` (already created for you):
```ini
FLASK_APP=app.py
FLASK_DEBUG=True
SECRET_KEY=edusmart-insecure-dev-key-change-in-production-2026
DATABASE_URL=sqlite:///instance/edusmart.db
GEMINI_API_KEY=your_gemini_api_key_here
MAX_CONTENT_LENGTH=10485760
UPLOAD_FOLDER=uploads
```

> **Note on Gemini AI:** If you do not have an API key right away, you can get a free key at [Google AI Studio](https://aistudio.google.com/). The rest of the platform (Authentication, Study Planner, Notes, Assignments, Analytics, Admin) works 100% locally even without an API key!

---

## 5. Running the Application

### Option A: Quick Start (Double-click or run script)
Simply run or double-click `run.bat` (Windows) or `run.ps1` (PowerShell):
```powershell
.\run.bat
```

### Option B: Terminal Command
Run directly with Python (auto-detects virtual environment packages):
```powershell
python app.py
```
Or explicitly using the virtual environment's Python:
```powershell
.\venv\Scripts\python.exe app.py
```

Open your browser and navigate to:
👉 **`http://127.0.0.1:5000`**

### Pre-configured Demo Accounts:
* **Student Account:**
  * **Username:** `student`
  * **Password:** `student123`
* **Administrator Account:**
  * **Username:** `admin`
  * **Password:** `admin123`

---

## 6. Running Automated Tests

To run the automated unit and integration test suite:
```powershell
python -m unittest discover tests
```
All tests execute in-memory with zero side effects on your production database.

---

## 7. University Viva & Capstone Defense Q&A

**Q1: Why did you use Flask rather than Django?**  
*Answer:* Flask follows a microframework philosophy that gives us fine-grained architectural control. By structuring it with Blueprints, an Application Factory, and SQLAlchemy ORM, we demonstrate a clear understanding of modular software architecture without the unnecessary auto-generated bloat of Django.

**Q2: How does the system handle AI errors or API rate limits?**  
*Answer:* The `AIService` class encapsulates all calls to Gemini inside structured `try-except` blocks. If the user's API quota is exhausted, the network is unreachable, or the key is absent, the application gracefully returns informative error banners without crashing or hallucinating fake answers.

**Q3: How is user data isolated?**  
*Answer:* Multi-tenancy is enforced at the query level. Every database query for notes, tasks, assignments, and quizzes filters explicitly by `user_id = session['user_id']`, ensuring users cannot access or tamper with other students' records.

**Q4: How are passwords stored securely?**  
*Answer:* Passwords are never saved in plain text. We utilize Werkzeug's cryptographic PBKDF2 with SHA-256 salted hashing (`generate_password_hash` and `check_password_hash`).
