from fastapi import FastAPI
from app.api.health import router as health_router
from app.config.config import get_settings
from app.schemas.film import FilmCreate, FilmResponse
from app.database import Base, engine
from app.handlers.films import router as films_router
from app.models.film import Film
from app.handlers.films import router as films_router
from app.handlers.reviews import router as reviews_router
from app.handlers.auth import router as auth_router
from app.handlers.users import router as users_router
from app.handlers.rating import router as rating_router
from app.models.review import Review
from app.models.rating import Rating
from app.models.user import User

from app.database import Base,engine
settings = get_settings()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)



app.include_router(films_router)
app.include_router(reviews_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(rating_router)

app.include_router(health_router)
@app.get("/")
def root():
    return {"message": f"{settings.app_name}is running"}