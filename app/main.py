from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import router as api_v1_router


app = FastAPI(
    title="Pharma API",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",           # при желании — документация только под /api/v1
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # или ["*"] на время разработки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ВСЕ роутеры v1 будут доступны под /api/v1/…
app.include_router(api_v1_router, prefix="/api/v1")

