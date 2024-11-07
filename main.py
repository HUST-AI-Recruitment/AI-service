from fastapi import FastAPI, File, UploadFile
from router import backend_router
from router import ai_router
import uvicorn
import router

app = FastAPI()
app.include_router(backend_router.router)
app.include_router(ai_router.router)

@app.get("/api/v1/health")
def get_health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)