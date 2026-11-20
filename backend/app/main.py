from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import Base, engine

# Import routers
from .api.auth import router as auth_router
from .api.documents import router as documents_router
from .api.analysis import router as analysis_router
from .api.obligations import router as obligations_router
from .api.comparison import router as comparison_router
from .api.compliance import router as compliance_router
from .api.assistant import router as assistant_router
from .api.reports import router as reports_router
from .api.analytics import router as analytics_router

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Intelligent Legal Document Understanding, Risk Detection and Decision Support System"
)

# Enable CORS for React frontend (Vite default ports 5173, 3000, 8000, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(documents_router, prefix=settings.API_V1_STR)
app.include_router(analysis_router, prefix=settings.API_V1_STR)
app.include_router(obligations_router, prefix=settings.API_V1_STR)
app.include_router(comparison_router, prefix=settings.API_V1_STR)
app.include_router(compliance_router, prefix=settings.API_V1_STR)
app.include_router(assistant_router, prefix=settings.API_V1_STR)
app.include_router(reports_router, prefix=settings.API_V1_STR)
app.include_router(analytics_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "platform": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "Online",
        "api_docs": "/docs"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
