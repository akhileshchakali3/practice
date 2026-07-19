import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

db = None
is_mock = False

def initialize_firebase():
    global db, is_mock
    # If already initialized, return the Firestore db client
    if firebase_admin._apps:
        db = firestore.client()
        return db

    cred_path = os.environ.get('FIREBASE_CREDENTIALS_PATH', 'firebase-service-account.json')
    cred_json_str = os.environ.get('FIREBASE_CREDENTIALS_JSON')

    if cred_json_str:
        try:
            cred_dict = json.loads(cred_json_str)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            print(">>> Firebase Admin SDK initialized via environment variable successfully.")
        except Exception as e:
            print(f">>> Failed to initialize Firebase using environment variable: {e}")
            db = None
    elif os.path.exists(cred_path):
        try:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            print(f">>> Firebase Admin SDK initialized via '{cred_path}' successfully.")
        except Exception as e:
            print(f">>> Failed to initialize Firebase using credentials file: {e}")
            db = None
    else:
        print("\n" + "="*80)
        print("[WARNING] Firebase Service Account credentials not found.")
        print("Starting application in [Local In-Memory Mock Database Mode] for preview.")
        print("To connect to actual Firestore:")
        print("1. Place your 'firebase-service-account.json' key in the root directory.")
        print("2. Or set the 'FIREBASE_CREDENTIALS_JSON' environment variable.")
        print("="*80 + "\n")
        db = None
        is_mock = True

    return db

initialize_firebase()
