import uvicorn
import json
import pathlib
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from cassandra.cqlengine.management import sync_table
from dotenv import load_dotenv
from . import db, utils
from .users.models import User
from .users.schemas import UserSignUpSchema, UserLoginSchema
from .shortcuts import render

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
    return render(request, "home.html", {"username":username})

@app.get("/login", response_class=HTMLResponse)
def login_get_view(request:Request):
    return render(request, "auth/login.html", {})


@app.post("/login", response_class=HTMLResponse)
def login_post_view(request:Request,
                    email:str=Form(...),
                    password:str=Form(...)):
    raw_data = {
        "email":email,
        "password":password,
    }
    data, errors = utils.validate_schema_data_or_error(raw_data, UserLoginSchema)
    print(data)
    return render(request, "auth/login.html",
                                       {
                                        "data":data,
                                        "errors":errors})

@app.get("/signup", response_class=HTMLResponse)
def signup_get_view(request:Request):
    return render(request, "auth/signup.html", {})


@app.post("/signup", response_class=HTMLResponse)
def signup_post_view(request:Request,
                    email:str=Form(...),
                    password:str=Form(...),
                    confirm_password:str=Form(...)):
    raw_data = {
        "email":email,
        "password":password,
        "confirm_password":confirm_password
    }
    data, errors = utils.validate_schema_data_or_error(raw_data, UserSignUpSchema)
    return render(request, "auth/signup.html",
                                    {"data": data,
                                    "errors":errors})

@app.get("/user")
def user_view_list():
    query = User.objects.all().limit(10)
    return list(query)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port="8000")