import firebase
import firebase_admin
import uvicorn
import requests

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from firebase_admin import auth

from firebase_helper import *
from misc_helper import *
from models import LoginSchema, SignUpSchema

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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

@app.post('/signup')
async def create_account(user_data: SignUpSchema):
    email = user_data.email
    password = user_data.password

    try:
        user = auth.create_user(
            email=email,
            password=password,
        )
        print('Sucessfully created new user: {0}'.format(user.uid))
        # print('user created', user)
        # Simpan data pengguna ke Firestore
        user_data_dict = {
            "email": user.email,
            "created_at": firestore.SERVER_TIMESTAMP
        }
        page = auth.list_users()
        print('user data dict', page)
        db.collection('users').document(user.uid).set(user_data_dict)

        return JSONResponse(
            content={
                "message": "User account created successfully!",
            }, status_code=201
        )

    except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=400,
            detail="Email already used!"
        )

@app.get('/list')
async def acc_list():
    page = auth.list_users()
    while page:
        for user in page.users:
            print('User: ' + user.uid)
    # Get next batch of users.
        page = page.get_next_page()
    for user in auth.list_users().iterate_all():
        print('User: ' + user.uid)
    # users = page.users
    print(type(page))

    return {"list": page}

@app.post('/login')
async def create_access_token(user_data: LoginSchema):
    email = user_data.email
    password = user_data.password
    try:
        # Login pengguna dengan Firebase Authentication
        print('auth start')
        user = firebase_admin.auth.sign_in_with_email_and_password(email, password)
        print('auth passed', user)
        # Ambil token ID pengguna 
        data = {
            "email": email,
            "password": password
        }
        
        user1 = find_user(data, db=db)
        print('user detected: ', user)
        token = user['idToken']
        print('token passed')
        # Verifikasi token ID 
        decoded_token = auth.verify_id_token(token)
        print('decoded token passed')
        # Ambil data pengguna dari Firestore
        user_ref = db.collection('users').document(decoded_token['uid'])
        user_data = user_ref.get().to_dict()

        if user_data:
            return JSONResponse(
                content={
                    "token": token,
                    "user": user_data
                }, status_code=200
            )
        else:
            raise HTTPException(
                status_code=404,
                detail="User data not found!"
            )

    except auth.AuthError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid Credentials! {e}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error! {e}"
        )

@app.post('/ping')
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
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
