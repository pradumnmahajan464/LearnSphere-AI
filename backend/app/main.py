"""
LearnSphere AI — FastAPI application entry point.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .database import engine, Base
from .routes import (
    auth_router, dashboard_router, subjects_router,
    quizzes_router, recommendations_router,
)

load_dotenv()

# Create tables on startup (idempotent)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LearnSphere AI",
    description="Personalized Learning Assistant API — UN SDG 4: Quality Education",
    version="1.0.0",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
# Allow the configured origin plus common local dev ports
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
allow_origins = [
    frontend_origin,
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(subjects_router)
app.include_router(quizzes_router)
app.include_router(recommendations_router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "service": "LearnSphere AI"}
@app.get("/")
def root():
    return {
        "message": "Welcome to LearnSphere AI",
        "status": "running",
        "docs": "/docs"
    }