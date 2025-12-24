from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import CodeInput
from router import analyze_by_language
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# -------------------- CORS --------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Health Check --------------------

@app.get("/")
def home():
    return {"message": "Backend is working!"}

# -------------------- Analyze Endpoint --------------------

@app.post("/analyze")
def analyze_code(data: CodeInput):
    """
    Receives code + language
    Routes to appropriate language analyzer
    """
    return analyze_by_language(data.language, data.code)
