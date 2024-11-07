from fastapi import FastAPI, File, UploadFile, APIRouter
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import os
from openai import OpenAI
from service import ai_service

router = APIRouter()
# AIScoreAPI = "http://localhost:8080/api/v1/ai_score"
api_config_path = os.path.join(os.path.dirname(__file__), "../config/api-key.json")
key = json.load(open(api_config_path))['api-key']
# use ali AI API, api-key should not leak, so put it in the config file
# and add the config file to .gitignore


@router.post("/api/v1/recommend_jobs")
def recommended_jobs_scoring(prompt: json):
    prompt = prompt["prompt"]
    score: int
    try:
        client = OpenAI(
            api_key = key,
            base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        # file_object = client.files.create(file=resume_file.file, purpose="file-extract")
        completion = client.chat.completions.create(
            model="qwen-turbo",
            messages=[
                {'role': 'system',
                 'content': {'type': 'text',
                             'text': 'You are to score the job and candidate based on the following information'}
                },
                {'role': 'user',
                 'content': {'type': 'text',
                             'text': prompt}
                }
            ]
        )
    except:
        return JSONResponse(content={"error": "Aliyun-connection-error"}, status_code=500)
    model_response = completion.model_dump_json()
    response_text = model_response['choices'][0]['message']['content']
    score = ai_service.AI_response_handler(response_text)
    return JSONResponse(content={"score": score}, status_code=200)


@router.post('/api/v1/rank_candidates')
def scoring_candidates(prompt: str, resume: UploadFile = File(...)):
    score: int
    try:
        client = OpenAI(
            api_key = key,
            base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        # file_object = client.files.create(file=resume.file, purpose="file-extract")
        completion = client.chat.completions.create(
            model="qwen-turbo",
            messages=[
                {'role': 'system',
                 'content': {'type': 'text',
                             'text': 'You are to score the candidate based on the following information'},
                },
                {'role': 'user',
                 'content': {'type': 'text',
                             'text': prompt}
                }
            ]
        )
    except:
        return JSONResponse(content={"error": "Aliyun-connection-error"}, status_code=500)
    model_response = completion.model_dump_json()
    response_text = model_response['choices'][0]['message']['content']
    score = ai_service.AI_response_handler(response_text)
    return JSONResponse(content={"score": score}, status_code=200)