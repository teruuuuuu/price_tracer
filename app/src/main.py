from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from log import logger
from scheduler.life_span import lifespan
from starlette.responses import RedirectResponse
from starlette import status
from routes import instruments_router

CURRENT_FILE_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(CURRENT_FILE_PATH)
STATIC_DIR = os.path.join(BASE_DIR, "static")


logger.info("Initializing FastAPI application...")
app = FastAPI(lifespan=lifespan)

# /static というURLパスで、./static ディレクトリのファイルを提供
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def serve_index():
    logger.info("Serving index.html - Redirecting to /static/index.html")
    return RedirectResponse(
        url="/static/index.html", 
        status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )

app.include_router(instruments_router.router)


logger.info("FastAPI application initialized.")