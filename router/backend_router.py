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


@router.post("/api/v1/recommend_jobs/resume")
def recommend_jobs_resume(post_data: json):
    recommend_config_path = config_path
    recommend_settings = json.load(open(recommend_config_path))
    recommend_number = recommend_settings["recommend_number"]
    resume = post_data["resume"]
    positions_data = post_data["jobs"]
    positions_score = []
    for position in positions_data:
        job_prompt = job.describe_job(position, mode="recommend-resume")
        player_prompt = job.describe_player(resume, mode="recommend-resume")
        prompt = player_prompt + job_prompt
        try:
            ai_score = requests.post(AIScorePositionAPI, json={"prompt": prompt}).json()
            if ai_score.status_code != 200:
                return JSONResponse(content={"error": "AI service error"}, status_code=500)
            ai_score = ai_score["score"]
        except:
            return JSONResponse(content={"error": "AI service error"}, status_code=500)
        positions_score.append({"id": position["id"], "ai_score": ai_score})
    positions_score = sorted(positions_score, key=lambda x: x["ai_score"], reverse=True)[:recommend_number]
    position_id = [position["id"] for position in positions_score]
    position_id = {"job": position_id}
    return JSONResponse(content=position_id, status_code=200) 

@router.post("/api/v1/recommend_jobs/description")
def recommend_jobs_resume(post_data: json):
    recommend_config_path = config_path
    recommend_settings = json.load(open(recommend_config_path))
    recommend_number = recommend_settings["recommend_number"]
    description = post_data["description"]
    positions_data = post_data["jobs"]
    positions_score = []
    for position in positions_data:
        job_prompt = job.describe_job(position, mode="recommend-description")
        player_prompt = job.describe_player(description, mode="recommend-description")
        prompt = player_prompt + job_prompt
        try:
            ai_score = requests.post(AIScorePositionAPI, json={"prompt": prompt}).json()
            if ai_score.status_code != 200:
                return JSONResponse(content={"error": "AI service error"}, status_code=500)
            ai_score = ai_score["score"]
        except:
            return JSONResponse(content={"error": "AI service error"}, status_code=500)
        positions_score.append({"id": position["id"], "ai_score": ai_score})
    positions_score = sorted(positions_score, key=lambda x: x["ai_score"], reverse=True)[:recommend_number]
    position_id = [position["id"] for position in positions_score]
    position_id = {"job": position_id}
    return JSONResponse(content=position_id, status_code=200) 


@router.post('/api/v1/rank_candidates')
def rank_candidates(post_data: json):
    # Setting the candidate number from config file
    candidate_config_path = config_path
    candidate_settings = json.load(open(candidate_config_path))
    candidate_number = candidate_settings["candidate-recommend-number"]
    candidates = []
    
    # extract datas from post_data
    resumes = post_data["resumes"]
    job = post_data["job"]
    job_prompt = job.describe_job(job, mode="rank-candidates")
    
    # rank the candidates
    for resume in resumes:
        player_prompt = job.describe_player(resume, mode="rank-candidates")
        prompt = job_prompt + player_prompt
        try:
            ai_score = requests.post(AIScoreCandidateAPI, json={"prompt": prompt}).json()
            if ai_score.status_code != 200:
                return JSONResponse(content={"error": "AI service error"}, status_code=500)
            ai_score = ai_score["score"]
            candidates.append({"id": resume["id"], "score": ai_score})
        except:
            return JSONResponse(content={"error": "AI service error"}, status_code=500)
    candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)[:candidate_number]
    return JSONResponse(content=candidates, status_code=200)

