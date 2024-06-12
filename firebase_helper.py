import firebase_admin
import dotenv, os
from firebase_admin import App, credentials, firestore, initialize_app, storage
from misc_helper import load_firebase_credentials

def init_firebase_app(env_file):
    try:
        app = firebase_admin.get_app()
    except ValueError as e:
        dotenv.load_dotenv(dotenv_path=env_file)

        # Initialize the configs for the Firebase Admin SDK
        firebase_config = {}
        firebase_config['apiKey'] = os.getenv('firebase_apiKey')
        firebase_config['authDomain'] = os.getenv('firebase_authDomain')
        firebase_config['projectId'] = os.getenv('firebase_projectId')
        firebase_config['storageBucket'] = os.getenv('firebase_storageBucket')
        firebase_config['messagingSenderId'] = os.getenv('firebase_messagingSenderId')
        firebase_config['appId'] = os.getenv('firebase_appId')
        firebase_config['measurementId'] = os.getenv('firebase_measurementId')
        firebase_config['serviceAccount'] = "firestore-credentials.json"
        cred_json = load_firebase_credentials(env_file)

        cred = credentials.Certificate(cred_json)
        app = firebase_admin.initialize_app(credential=cred, options=firebase_config)
    return app

def init_firestore(env_file, app = None):
    if app is None:
        app = init_firebase_app(env_file)
    db = firestore.client(app)
    return db

def init_storage(env_file, app = None):
    if app is None:
        app = init_firebase_app(env_file)
        print("App type: ", type(app))
    storage_instance = storage.bucket(name="bangkit-capstone-dms.appspot.com", app=app)
    return storage_instance

def add_test_data(collection_name, data, db = None):
    if db is None:
        db = init_firestore('.env')
    # Add a new document with a generated ID
    db.collection(collection_name).add(data)
    print("Document added successfully")

def add_driver_frame(bytes, driver_id, timestamp, storage = None):
    if storage is None:
        print("Storage initialized")
        storage = init_storage('.env')
    print(type(storage))
    try:
        filename = str(driver_id + "_" + timestamp + ".jpg")
        destination_blob_path = "frames/" + filename
        blob = storage.blob(destination_blob_path)
        blob.upload_from_string(bytes, content_type='image/jpg')
        blob.make_public()
        print("File added successfully")
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "Frame not added successfully"}