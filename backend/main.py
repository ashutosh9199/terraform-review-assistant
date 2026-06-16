from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from api.routers import upload, analyze

app = FastAPI(
    title="AI-Powered Terraform Review Assistant",
    description="API for reviewing and scoring Terraform infrastructure.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

app.include_router(upload.router, prefix="/api/v1/upload", tags=["Upload"])
app.include_router(analyze.router, prefix="/api/v1/analyze", tags=["Analyze"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}
