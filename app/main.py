from fastapi import FastAPI

from app.api.health import router as health_router
from app.config.config import get_settings


settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)


app.include_router(health_router)


@app.get("/")
def root():
    return {
        "message": f"{settings.app_name} is running",
    }



@app.get("/hello")
def hello():
    return {
        "message": "Hello, FastAPI!",
    }



from app.api.items import router as items_router

app.include_router(items_router)