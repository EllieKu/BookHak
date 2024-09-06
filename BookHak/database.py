import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Firestore Admin SDK key
key = "firebase-adminsdk.json"

cred = credentials.Certificate(key)
app = firebase_admin.initialize_app(cred)
db = firestore.client()
