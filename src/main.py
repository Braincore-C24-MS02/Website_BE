import firebase_admin
import pyrebase
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from firebase_admin import auth, credentials
from models import LoginSchema, SignUpSchema

app = FastAPI(
    description="test",
    title="Login Page",
    docs_url="/"
)

# Konfigurasi CORS agar dapat diakses dari frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Ganti dengan URL frontend kamu misalnya ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not firebase_admin._apps:
    cred = credentials.Certificate("../serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

firebaseConfig = {
  "apiKey": "AIzaSyAFYEUUziI12WWTrFgR3omCKDFuy-jBnPU",
  "authDomain": "bangkit-capstone-dms.firebaseapp.com",
  "projectId": "bangkit-capstone-dms",
  "storageBucket": "bangkit-capstone-dms.appspot.com",
  "messagingSenderId": "987502499591",
  "appId": "1:987502499591:web:7cd1c908910dd73b4a17a2",
  "measurementId": "G-8Y7NLPFNC9",
  "databaseURL" : ""
}

firebase = pyrebase.initialize_app(firebaseConfig)

@app.post('/Signup')
async def create_account(user_data: SignUpSchema):
    email = user_data.email
    password = user_data.password

    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return JSONResponse(
            content={
                "message": "User account created successfully!"
            }, status_code=201
        )

    except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=400,
            detail="Email already used!"
        )

@app.post('/Login')
async def create_access_token(user_data: LoginSchema):
    email = user_data.email
    password = user_data.password

    try:
        user = firebase.auth().sign_in_with_email_and_password(
            email=email,
            password=password
        )

        token = user['idToken']

        return JSONResponse(
            content={
                "token": token
            }, status_code=200
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid Credentials!"
        )

@app.post('/Ping')
async def validate_token(request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    
    if jwt:
        try:
            user = auth.verify_id_token(jwt)
            return user
        except Exception as e:
            raise HTTPException(
                status_code=403,
                detail="Invalid token"
            )
    else:
        raise HTTPException(
            status_code=403,
            detail="Token not provided"
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
