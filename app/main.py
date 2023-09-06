from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
from cassandra.cqlengine.management import sync_table
from . import config, db
from .users.models import User

load_dotenv(".env")
DB_SESSION = None
app = FastAPI()
# settings = config.get_settings()

@app.on_event("startup")
def on_startup():
    global DB_SESSION
    #Triggered when fastapi starts
    print("Hello world!!")
    DB_SESSION = db.get_session()
    sync_table(User)

@app.get("/")
def homepage():
    return {
        "message": "Welcome to my Homepage"
    }

@app.get("/user")
def user_view_list():
    query = User.objects.all().limit(10)
    return list(query)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port="8000")
