from fastapi import FastAPI, File, UploadFile, Response
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from service import job
import requests
from typing import List
import json
import os

router = APIRouter()
GetAllPositionAPI = "http://localhost:8080/api/v1/jobs"
AIScorePositionAPI = "http://localhost:8080/api/v1/recommend_jobs"
AIScoreCandidateAPI = "http://localhost:8080/api/v1/rank_candidates"
config_path = os.path.join(os.path.dirname(__file__), "../config/settings.json")


@router.post("/api/v1/recommend_jobs")
def recommend_jobs(resume_file: UploadFile = File(...)):
    # curl -X POST http://localhost:5000/recommend_jobs -F "resume_file=@/path/to/resume.pdf"
    recommend_config_path = config_path
    recommend_settings = json.load(open(recommend_config_path))
    recommend_number = recommend_settings["recommend_number"]
    positions_data = requests.get(GetAllPositionAPI).json()
    positions_score = []
    for position in positions_data:
        text_prompt = job.describe_job(position)
        try:
            ai_score = requests.post(AIScorePositionAPI, json={"prompt": text_prompt, "resume_file": resume_file.file}).json()
            if ai_score.status_code != 200:
                return JSONResponse(content={"error": "AI service error"}, status_code=500)
            ai_score = ai_score["score"]
        except:
            return JSONResponse(content={"error": "AI service error"}, status_code=500)
        positions_score.append({"position": position, "ai_score": ai_score})
    positions_score = sorted(positions_score, key=lambda x: x["ai_score"], reverse=True)[:recommend_number]
    return JSONResponse(content=positions_score, status_code=200)


@router.post('/api/v1/rank_candidates')
def rank_candidates(job: dict, resume_files: List[UploadFile] = File(...)):
    candidate_config_path = config_path
    candidate_settings = json.load(open(candidate_config_path))
    candidate_number = candidate_settings["candidate-recommend-number"]
    candidates = []
    for resume in resume_files:
        text_prompt = job.describe_job(job)
        try:
            ai_score = requests.post(AIScoreCandidateAPI, json={"prompt": text_prompt, "resume_file": resume.file}).json()
            if ai_score.status_code != 200:
                return JSONResponse(content={"error": "AI service error"}, status_code=500)
            ai_score = ai_score["score"]
            candidates.append({"resume": resume, "score": ai_score})
        except:
            return JSONResponse(content={"error": "AI service error"}, status_code=500)
    candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)[:candidate_number]
    return JSONResponse(content=candidates, status_code=200)

