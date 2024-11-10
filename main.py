from fastapi import FastAPI, File, UploadFile
from router import backend_router
from router import ai_router
import uvicorn
import router
import os
import json

app = FastAPI()
app.include_router(backend_router.router)
app.include_router(ai_router.router)

settings_config_path = os.path.join(os.path.dirname(__file__), "./config/settings.json")
port = json.load(open(settings_config_path))['port']

@app.get("/api/v1/health")
def get_health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="ai", port=port)
