from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from service import job
import requests
from typing import List
import json

router = APIRouter()
GetAllPositionAPI = "http://localhost:8080/api/v1/jobs"
AIScoreAPI = "http://localhost:8080/api/v1/ai_score"

@router.post("/api/v1/recommend_jobs")
def recommend_jobs(resume_file: UploadFile = File(...)):
    # curl -X POST http://localhost:5000/recommend_jobs -F "resume_file=@/path/to/resume.pdf"
    positions_data = requests.get(GetAllPositionAPI).json()
    positions_score = []
    for position in positions_data:
        text_prompt = job.describe_job(position)
        ai_score = requests.post(AIScoreAPI, json={"prompt": text_prompt, "resume_file": resume_file.file}).json()
        ai_score = ai_score["score"]
        positions_score.append({"position": position, "ai_score": ai_score})
    positions_score = sorted(positions_score, key=lambda x: x["ai_score"], reverse=True)[:5]
    return JSONResponse(content=positions_score)

class job(BaseModel):
    title: str
    description: str
    location: str
    salary: float
    company_name: str
    create_at: str

@router.post('/api/v1/rank_candidates')
def rank_candidates(job: job, resume_files: List[UploadFile] = File(...)):
    pass