from fastapi import FastAPI

from src.router import app_router as apiRouter

def createApp() -> FastAPI:
    app = FastAPI()
    return app

app = createApp()
app.include_router(apiRouter.router, prefix = "/api")