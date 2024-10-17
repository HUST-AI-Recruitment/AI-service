from fastapi import FastAPI, File, UploadFile
from router import backend

app = FastAPI()
app.include_router(backend.router)

@app.get("/api/v1/health")
def get_health():
    return {"status": "ok"}

