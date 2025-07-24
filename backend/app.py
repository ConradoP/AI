from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
import json, os

app = FastAPI()
BASE_DIR = "backend/chatlogs"
USERS_DB = "backend/users.json"

os.makedirs(BASE_DIR, exist_ok=True)

def load_users():
    if not os.path.exists(USERS_DB): return {}
    with open(USERS_DB, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_DB, "w") as f:
        json.dump(users, f)

def get_user_file(user_id):
    return os.path.join(BASE_DIR, f"{user_id}.json")

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    users = load_users()
    if username in users and users[username] == password:
        with open(get_user_file(username), "a") as f: pass
        return {"message": "Login successful", "user_id": username}
    return JSONResponse(status_code=401, content={"message": "Invalid credentials"})

@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):
    users = load_users()
    if username in users:
        return JSONResponse(status_code=400, content={"message": "User already exists"})
    users[username] = password
    save_users(users)
    return {"message": "Registered successfully", "user_id": username}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    message = data.get("message")
    chat_file = get_user_file(user_id)
    with open(chat_file, "a") as f:
        f.write(json.dumps({"user": message}) + "\n")
    return {"response": f"Você disse: {message}"}