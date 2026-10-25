from fastapi import FastAPI

from src.routes import router

app = FastAPI()
app.include_router(router=router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy"}