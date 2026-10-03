import os
from fastapi import FastAPI, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

app = FastAPI()

# Static files live in public/ so Vercel serves them from its CDN instead of the function.
# This mount is only used for local development.
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(ROOT_DIR, "public", "static"), check_dir=False),
    name="static"
)

templates = Jinja2Templates(directory=os.path.join(ROOT_DIR, "templates"))

@app.api_route("/", methods=["GET", "HEAD"])
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        headers={"Cache-Control": "public, max-age=0, s-maxage=86400, stale-while-revalidate=604800"},
    )



@app.exception_handler(StarletteHTTPException)
async def cached_http_exception(request: Request, exc: StarletteHTTPException):
    # Let the edge cache 404s so bots probing random paths don't each invoke the function.
    response = await http_exception_handler(request, exc)
    if exc.status_code == 404:
        response.headers["Cache-Control"] = "public, max-age=0, s-maxage=3600"
    return response
