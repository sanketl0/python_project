from fastapi import FastAPI, File, UploadFile
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.post("/")
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()
    rows = contents.decode("utf-8").split("\n")
    headers = rows[0].split(",")
    name_index = headers.index("Name")
    age_index = headers.index("Age")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER)")

    for row in rows[1:]:
        name = row.split(",")[name_index]
        age = row.split(",")[age_index]

        c.execute("INSERT INTO Users (name, age) VALUES (?, ?)", (name, age))

    conn.commit()
    conn.close()

    return {"message": "File uploaded successfully"}

@app.get("/")
async def index():
    return templates.TemplateResponse("index.html", {"request": request})