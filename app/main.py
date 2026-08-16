import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(ROOT_DIR, "static")),
    name="static"
)

templates = Jinja2Templates(directory=os.path.join(ROOT_DIR, "templates"))

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")
