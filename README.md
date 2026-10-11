# 🎓 LearnSphere AI — Personalized Learning Assistant

> **UN SDG 4: Quality Education** | Full-stack web application for students to track progress, take quizzes, and receive personalized study recommendations.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Prerequisites](#prerequisites)
5. [Backend Setup](#backend-setup)
6. [Frontend Setup](#frontend-setup)
7. [Running the Application](#running-the-application)
8. [API Documentation](#api-documentation)
9. [Features](#features)
10. [Architecture](#architecture)

---

## Project Overview

LearnSphere AI helps students:
- Track learning progress across subjects (Python, ML, Data Structures, Mathematics)
- Take multiple-choice quizzes with backend-validated scoring
- Identify weak areas based on quiz performance
- Receive personalized recommendations using a rule-based engine

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, TypeScript, Vite, Tailwind CSS |
| Charts | Recharts |
| Icons | Lucide React |
| HTTP Client | Axios |
| Backend | Python 3.10+, FastAPI, Uvicorn |
| Database | SQLite (via SQLAlchemy) |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Validation | Pydantic v2 |
| ML/Recommendations | Rule-based engine (scikit-learn available) |
| Testing | pytest, httpx |

---

## Project Structure

```
LearnSphere-AI/
├── app/                        # React frontend (Vite + TypeScript)
│   ├── src/
│   │   ├── components/         # Sidebar, Layout, ProgressBar, etc.
│   │   ├── pages/              # Login, Register, Dashboard, Subjects, Quizzes, etc.
│   │   ├── services/           # Axios API service layer
│   │   ├── types/              # TypeScript interfaces
│   │   ├── App.tsx             # Router and route guards
│   │   └── main.tsx            # Entry point
│   ├── package.json
│   └── .env.example
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── routes/             # auth, dashboard, subjects, quizzes, recommendations
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   ├── services/           # JWT auth helpers
│   │   ├── ml/                 # Rule-based recommendation engine
│   │   ├── database.py         # Engine, session, Base
│   │   └── main.py             # FastAPI app, CORS, routers
│   ├── seed.py                 # Database seed script
│   ├── tests/test_app.py       # pytest test suite
│   ├── requirements.txt
│   └── .env.example
├── README.md
└── .gitignore
```

---

## Prerequisites

- **Python 3.10+** — [python.org](https://www.python.org/downloads/)
- **Node.js 18+** — [nodejs.org](https://nodejs.org/)
- **npm** (comes with Node.js)

---

## Backend Setup

```bash
# 1. Navigate to the backend directory
cd LearnSphere-AI/backend

# 2. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create the environment file
copy .env.example .env        # Windows
cp .env.example .env          # macOS/Linux

# Edit .env if needed (the defaults work out-of-the-box)

# 5. Seed the database with sample content
python seed.py

# 6. Start the backend server
uvicorn app.main:app --reload --port 8000
```

The backend will be available at **http://localhost:8000**

API documentation (Swagger UI): **http://localhost:8000/docs**

---

## Frontend Setup

```bash
# 1. Navigate to the frontend directory
cd LearnSphere-AI/app

# 2. Install dependencies
npm install

# 3. Create the environment file
copy .env.example .env.local        # Windows
cp .env.example .env.local          # macOS/Linux

# 4. Start the development server
npm run dev
```

The frontend will be available at **http://localhost:5173**

---

## Running the Application

You need **two terminal windows** running simultaneously:

**Terminal 1 — Backend:**
```bash
cd LearnSphere-AI/backend
venv\Scripts\activate        # or source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd LearnSphere-AI/app
npm run dev
```

Then open **http://localhost:5173** in your browser.

### First Time

1. Click **Create one** on the login page.
2. Register with any name, email, and password (min. 6 characters).
3. You will be automatically logged in and redirected to the dashboard.

---

## API Documentation

FastAPI provides interactive documentation at:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new student |
| POST | `/api/auth/login` | Login and receive JWT token |
| GET | `/api/auth/me` | Get current user info |
| GET | `/api/dashboard` | Dashboard summary |
| GET | `/api/subjects` | List all subjects |
| GET | `/api/subjects/{id}` | Subject detail with topics |
| POST | `/api/topics/{id}/complete` | Mark topic as completed |
| GET | `/api/quizzes` | List all quizzes |
| GET | `/api/quizzes/{id}` | Quiz questions (no answers exposed) |
| POST | `/api/quizzes/{id}/submit` | Submit answers, get score |
| GET | `/api/quiz-attempts` | All quiz attempts for current user |
| GET | `/api/recommendations` | Personalized recommendations |
| GET | `/health` | Health check |

All endpoints except `/api/auth/register`, `/api/auth/login`, and `/health` require a Bearer token.

---

## Features

### 1. Student Login & Registration
- Secure password hashing with bcrypt
- JWT-based authentication (60-minute tokens)
- Protected routes with automatic redirect

### 2. Student Dashboard
- Welcome message, stat cards (subjects, quiz average, lessons completed)
- Subject progress bar chart (Recharts)
- Recent quiz results with colour-coded accuracy
- AI-recommended next topic

### 3. Subjects & Learning Materials
- 4 subjects: Python Programming, Machine Learning, Data Structures, Mathematics
- 4 topics per subject with detailed notes
- Difficulty levels: Beginner / Intermediate / Advanced
- Per-student topic completion tracking

### 4. Quizzes & Performance Tracking
- 2 quizzes per subject (8 quizzes total, 5 questions each = 40 questions)
- Answers validated **on the backend** — correct answers never sent to frontend
- Per-question explanations shown after submission
- Complete attempt history with scores and dates

### 5. Personalized Recommendations
- Rule-based engine in `backend/app/ml/recommender.py`
- Thresholds: `< 50%` → revise | `50–79%` → practice | `≥ 80%` → advance
- Shows reason and suggested action per subject
- Updates automatically after each quiz attempt

---

## Running Tests

```bash
cd LearnSphere-AI/backend
venv\Scripts\activate
pytest tests/ -v
```

Tests cover:
- User registration and duplicate detection
- Login with correct/wrong credentials
- JWT-protected endpoints
- Quiz scoring (perfect score, zero score, wrong answer count)
- Correct answers not exposed before submission
- Recommendations for new users, high scorers, and low scorers
- Health check endpoint

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `insecure-default-key-change-me` | JWT signing key — change in production |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Token expiry |
| `DATABASE_URL` | `sqlite:///./learnsphere.db` | Database connection string |
| `FRONTEND_ORIGIN` | `http://localhost:5173` | Allowed CORS origin |

### Frontend (`app/.env.local`)

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_URL` | `http://localhost:8000` | Backend API base URL |

---

## Security Notes

- Passwords are hashed with bcrypt (via passlib) — never stored in plain text.
- JWT tokens expire after 60 minutes.
- Correct quiz answers are **never sent** to the frontend until after submission.
- All private endpoints verify the JWT token.
- Students can only access their own data.
- `.env` files are excluded from version control.

---

*Built as a college project demonstrating full-stack web development, REST APIs, and rule-based AI recommendations in support of UN SDG 4: Quality Education.*
