from fastapi import FastAPI, File, UploadFile
from router import backend
import uvicorn

app = FastAPI()
app.include_router(backend.router)

@app.get("/api/v1/health")
def get_health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)