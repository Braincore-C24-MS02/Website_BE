import os

import firebase_admin
import pyrebase
import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from firebase_admin import auth, credentials, firestore
from firebase_helper import init_firebase_app, init_firestore, init_storage
from misc_helper import parse_datetime
from models import LoginSchema, SignUpSchema

# Muat variabel lingkungan dari .env file
load_dotenv()

app = FastAPI()

origins = ['http://localhost:8080/']



# Tambahkan middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Ganti dengan URL frontend Anda
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# Inisialisasi Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": os.getenv("fc_type"),
        "project_id": os.getenv("fc_project_id"),
        "private_key_id": os.getenv("fc_private_key_id"),
        "private_key": os.getenv("fc_private_key").replace('\\n', '\n'),
        "client_email": os.getenv("fc_client_email"),
        "client_id": os.getenv("fc_client_id"),
        "auth_uri": os.getenv("fc_auth_uri"),
        "token_uri": os.getenv("fc_token_uri"),
        "auth_provider_x509_cert_url": os.getenv("fc_auth_provider_x509_cert_url"),
        "client_x509_cert_url": os.getenv("fc_client_x509_cert_url"),
        "universe_domain": os.getenv("fc_universe_domain")
    })
    firebase_admin.initialize_app(cred)

# Inisialisasi Pyrebase
firebaseConfig = {
    "apiKey": os.getenv("firebase_apiKey"),
    "authDomain": os.getenv("firebase_authDomain"),
    "projectId": os.getenv("firebase_projectId"),
    "storageBucket": os.getenv("firebase_storageBucket"),
    "messagingSenderId": os.getenv("firebase_messagingSenderId"),
    "appId": os.getenv("firebase_appId"),
    "measurementId": os.getenv("firebase_measurementId"),
    "databaseURL" : ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth_pyrebase = firebase.auth()

# Inisialisasi Firestore
firebase_app = init_firebase_app('.env')
db = init_firestore(env_file='.env', app=firebase_app)

@app.get("/")
async def root():
    return {"message": "Website_BE is running"}

@app.get("/")
async def root():
    return {"message": "Website_BE is running"}

@app.post('/Signup')
async def create_account(user_data: SignUpSchema):
    email = user_data.email
    password = user_data.password
    name = user_data.name  

    try:
        
        user = auth.create_user(
            email=email,
            password=password,
            display_name=name  
        )
        
        user_data_dict = {
            "name": name,  
            "email": email,
            "created_at": firestore.SERVER_TIMESTAMP
        }
        db.collection('users').document(user.uid).set(user_data_dict)

        return JSONResponse(
            content={"message": "User account created successfully!"},
            status_code=201
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

@app.options("/Login")
async def login_options():
    return JSONResponse(
        content="Allowed",
        status_code=200,
        headers={"Allow": "POST"}
    )



# @app.post('/login')
# async def login(user_data: LoginSchema):
#     email = user_data.email
#     password = user_data.password

#     try:
#         # Login pengguna dengan Firebase Authentication
#         user = auth.sign_in_with_email_and_password(email, password)

#         # Ambil token ID pengguna
#         token = user['idToken']

#         # Kembalikan token sebagai respons
#         return JSONResponse(
#             content={"token": token},
#             status_code=200
#         )

#     except auth.InvalidEmailError:
#         raise HTTPException(
#             status_code=400,
#             detail="Email tidak valid!"
#         )

#     except auth.WrongPasswordError:
#         raise HTTPException(
#             status_code=400,
#             detail="Password salah!"
#         )

#     except auth.UserNotFoundError:
#         raise HTTPException(
#             status_code=404,
#             detail="Pengguna tidak ditemukan!"
#         )

#     except auth.NotAllowedError:
#         raise HTTPException(
#             status_code=403,
#             detail="Login tidak diizinkan untuk pengguna ini!"
#         )

#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Terjadi kesalahan internal: {str(e)}"
#         )

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

@app.post("/send/send-message")
async def send_message(userID, driverID, message: str):
    try:
        user_id = userID
        driver_id = driverID
        timestamp_url = "http://worldtimeapi.org/api/timezone/Asia/Jakarta"
        response = requests.get(timestamp_url).json()
        timestamp = str(parse_datetime(response['datetime']))
        data = {
            "sender-id": user_id,
            "receiver-id": driver_id,
            "message": message,
            "timestamp": timestamp
        }
        db.collection('messages').add(data)
        return {"message": "Data added successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=f"Error: {e}")

@app.post("/send/send-alert")
async def send_alert(userID, driverID):
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
        db.collection('alerts').add(data)
        return {"message": "Data added successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=f"Error: {e}")
    
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
