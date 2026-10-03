import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        headers={"Cache-Control": "public, max-age=0, s-maxage=3600"},
    )
