import firebase
import uvicorn
import requests

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from firebase_admin import auth, credentials
from models import LoginSchema, SignUpSchema

from firebase_helper import *
from misc_helper import *

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Ganti dengan URL frontend kamu misalnya ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

firebase_app = init_firebase_app('.env')
db = init_firestore(env_file='.env', app=firebase_app)
storage = init_storage(env_file='.env', app=firebase_app)

@app.get("/")
async def root():
    return {"message": "Website_BE is running"} 

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

############################################################################################################
# FOR MESSAGES & ALERTS
############################################################################################################

@app.post("/send/send-message") #TODO: perlu tambahin id driver yg di-alert
async def send_data(userID, driverID, message: str):
    try:
        user_id = userID        #TODO: 
        driver_id = driverID   #Change hardcode to actual implementation later on
        timestamp_url = "http://worldtimeapi.org/api/timezone/Asia/Jakarta"
        response = requests.get(timestamp_url).json()
        timestamp = str(parse_datetime(response['datetime']))
        data = {
            "sender-id": user_id,
            "receiver-id": driver_id, 
            "message": message,
            "timestamp": timestamp
        }
        add_test_data('messages', data, db=db)
        return {"message": "Data added successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=f"Error: {e}")

@app.post("/send/send-alert") #TODO: perlu tambahin id driver yg di-alert
async def send_data(userID, driverID):
    try:
        user_id = userID     
        driver_id = driverID
        timestamp_url = "http://worldtimeapi.org/api/timezone/Asia/Jakarta"
        response = requests.get(timestamp_url).json()
        timestamp = str(parse_datetime(response['datetime']))
        data = {
            "sender-id": user_id,
            "receiver-id": driver_id, 
            "message": "ALERT",
            "timestamp": timestamp
        }
        add_test_data('alerts', data, db=db)
        return {"message": "Data added successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=f"Error: {e}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
