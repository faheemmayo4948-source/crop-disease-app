from lib.firebase_client import get_db
from firebase_admin import firestore


def save_farmer_profile(uid, land_size, land_unit, crops, location):
    db = get_db()
    db.collection("farmer_profiles").document(uid).set({
        "landSize": land_size,
        "landUnit": land_unit,
        "crops": crops,
        "location": location,
        "updatedAt": firestore.SERVER_TIMESTAMP,
    })


def get_farmer_profile(uid):
    db = get_db()
    doc = db.collection("farmer_profiles").document(uid).get()
    return doc.to_dict() if doc.exists else None
