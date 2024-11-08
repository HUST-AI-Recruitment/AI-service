from fastapi import FastAPI, File, UploadFile, APIRouter
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import os
from openai import OpenAI
from service import ai_service

router = APIRouter()

api_config_path = os.path.join(os.path.dirname(__file__), "../config/api-key.json")
key = json.load(open(api_config_path))['api-key']
# use ali AI API, api-key should not leak, so put it in the config file
# and add the config file to .gitignore

aliyun_dashscope_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"

class PROMPT(BaseModel):
    prompt: str

@router.post("/api/v1/recommend_jobs/ai")
def recommended_jobs_scoring(prompt: PROMPT):
    prompt = prompt.prompt
    try:
        client = OpenAI(
            api_key = key,
            base_url = aliyun_dashscope_url,
        )
        completion = client.chat.completions.create(
            model="qwen-turbo",
            response_format={"type": "json_object"},
            messages=[
                { 'role': 'system', 'content': 'You are to score the job and candidate based on the following information' },
                { 'role': 'user', 'content': prompt }
            ]
        )
    except Exception as e:
        return JSONResponse(content={"error": f"Aliyun-connection-error {e}"}, status_code=502)
    model_response = completion.model_dump_json()
    response_text = model_response['choices'][0]['message']['content']
    score = ai_service.AI_response_handler(response_text)
    return JSONResponse(content={"score": score}, status_code=200)


@router.post('/api/v1/rank_candidates')
def scoring_candidates(prompt: PROMPT):
    prompt = prompt.prompt
    try:
        client = OpenAI(
            api_key = key,
            base_url = aliyun_dashscope_url,
        )
        completion = client.chat.completions.create(
            model="qwen-turbo",
            response_format="json_object",
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
        return JSONResponse(content={"error": "Aliyun-connection-error"}, status_code=502)
    model_response = completion.model_dump_json()
    response_text = model_response['choices'][0]['message']['content']
    score = ai_service.AI_response_handler(response_text)
    return JSONResponse(content={"score": score}, status_code=200)