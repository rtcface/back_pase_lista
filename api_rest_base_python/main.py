from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from decouple import config
from utils.init_db import init_db
from router.api import router
from config.settings import settings

app = FastAPI(
    debug=bool(settings.DEBUG),
    title=settings.TITLE,
    description="FastAPI",
)

if settings.DEBUG:
    origins = ["*"]
else:
    origins = [
        str(origin).strip(",") for origin in settings.CORS_ALLOWED_ORIGINS
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup() -> None:
    """Start the application."""
    init_db()


app.include_router(router)


app.mount("/static", StaticFiles(directory="static"), name="static")
Message = settings.TITLE
@app.get("/")
def root():
    return {"Api": Message}
