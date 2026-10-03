from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
import sqlite3
import jwt

app = FastAPI(title="Moneyview Vulnerable Lending API", version="1.0.0")

# VULNERABILITY 1: Hardcoded Secret (Will be caught by custom Semgrep rule & Secret Scanner)
JWT_SECRET = "super_secret_moneyview_key_123!"

# In-memory DB setup for demonstration
conn = sqlite3.connect(':memory:', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, balance REAL, loan_amount REAL)''')
cursor.execute('''INSERT INTO users (id, username, balance, loan_amount) VALUES (1, 'alice', 1000.0, 500.0)''')
cursor.execute('''INSERT INTO users (id, username, balance, loan_amount) VALUES (2, 'bob', 50.0, 5000.0)''')
conn.commit()

class LoginRequest(BaseModel):
    username: str

@app.post("/api/v1/login")
def login(req: LoginRequest):
    # Dummy login just to generate a token
    cursor.execute(f"SELECT id FROM users WHERE username = '{req.username}'")
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generate token with hardcoded secret
    token = jwt.encode({"user_id": user[0]}, JWT_SECRET, algorithm="HS256")
    return {"access_token": token.decode('utf-8') if isinstance(token, bytes) else token}

@app.get("/api/v1/user/{user_id}/loan")
def get_loan_details(user_id: int, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        token = authorization.split("Bearer ")[1]
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        requester_id = payload.get("user_id")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    # VULNERABILITY 2: Broken Object Level Authorization (BOLA)
    # We authenticate the user, but we DON'T check if requester_id == user_id
    # A user can fetch another user's loan details!
    
    # VULNERABILITY 3: SQL Injection (Will be caught by SAST)
    query = f"SELECT username, loan_amount FROM users WHERE id = {user_id}"
    cursor.execute(query)
    result = cursor.fetchone()
    
    if not result:
         raise HTTPException(status_code=404, detail="Loan not found")
         
    return {"username": result[0], "loan_amount": result[1]}

@app.get("/health")
def health_check():
    return {"status": "ok"}
