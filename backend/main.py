from fastapi import FastAPI
from backend.routes.search import router as search_router

app = FastAPI()   #启动一个网站服务器

@app.get("/")
def root():
    return {
        "app": "AI Citation Finder",
        "status": "running",
        "docs": "/docs"
    }

app.include_router(search_router)