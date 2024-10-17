from fastapi import FastAPI, File, UploadFile, APIRouter
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json

router = APIRouter()
# AIScoreAPI = "http://localhost:8080/api/v1/ai_score"

@router.post("/api/v1/recommend_jobs")
def scoring(prompt: str, resume_file: UploadFile = File(...)):
    score: int
    # TODO
    
    return JSONResponse(content={"score": score})