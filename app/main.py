import uvicorn
import pathlib
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from cassandra.cqlengine.management import sync_table
from . import db
from .users.models import User


DB_SESSION = None
BASE_DIR = pathlib.Path(__file__).resolve().parent # app/
TEMPLATE_DIR = BASE_DIR / "templates"

app = FastAPI()
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))
load_dotenv(".env")


@app.on_event("startup")
def on_startup():
    global DB_SESSION
    #Triggered when fastapi starts
    DB_SESSION = db.get_session()
    sync_table(User)

@app.get("/", response_class=HTMLResponse)
def homepage(request:Request):
    username = "Igwe Miracle"
    return templates.TemplateResponse("home.html", {"request":request, "username":username})

@app.get("/login", response_class=HTMLResponse)
def login_get_view(request:Request):
    return templates.TemplateResponse("auth/login.html", {"request":request})


@app.post("/login", response_class=HTMLResponse)
def login_post_view(request:Request, email:str=Form(...),
                   password:str=Form(...)):
    print(email, password)
    return templates.TemplateResponse("auth/login.html", {"request":request})

@app.get("/user")
def user_view_list():
    query = User.objects.all().limit(10)
    return list(query)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port="8000")