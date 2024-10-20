from fastapi import FastAPI, File, UploadFile, APIRouter
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import os
from openai import OpenAI

router = APIRouter()
# AIScoreAPI = "http://localhost:8080/api/v1/ai_score"
api_config_path = os.path.join(os.path.dirname(__file__), "../config/api-key.json")
api_key = json.load(open(api_config_path))['api-key']
# use ali AI API, api-key should not leak, so put it in the config file
# and add the config file to .gitignore

@router.post("/api/v1/recommend_jobs")
def recommended_jobs_scoring(prompt: str, resume_file: UploadFile = File(...)):
    score: int
    # TODO
    
    return JSONResponse(content={"score": score}, status_code=200)

@router.post('/api/v1/rank_candidates')
def scoring_candidates(prompt: str, resume: UploadFile = File(...)):
    score: int
    # TODO
    return JSONResponse(content={"score": score}, status_code=200)