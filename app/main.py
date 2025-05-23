from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import history_router, question_router

app = FastAPI(title="LLM Integration API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(
    question_router.router,
    prefix="/api/v1",
    tags=["Question Generation"]
)

app.include_router(
    history_router.router,
    prefix="/api/v1",
    tags=["Generation History"]
)

@app.get("/")
def health_check():
    return {"status": "OK"}