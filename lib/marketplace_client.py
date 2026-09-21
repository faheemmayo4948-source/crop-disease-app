import streamlit as st
from lib.firebase_client import get_db
from firebase_admin import firestore


def request_seller_access(uid, email, business_name, business_type, contact):
    db = get_db()
    db.collection("sellers").document(uid).set({
        "email": email,
        "businessName": business_name,
        "businessType": business_type,
        "contact": contact,
        "status": "Pending",
        "createdAt": firestore.SERVER_TIMESTAMP,
    })


def get_seller_status(uid):
    db = get_db()
    doc = db.collection("sellers").document(uid).get()
    return doc.to_dict() if doc.exists else None


def get_all_sellers():
    db = get_db()
    docs = db.collection("sellers").stream()
    sellers = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        sellers.append(data)
    return sellers


def update_seller_status(seller_uid, status):
    db = get_db()
    db.collection("sellers").document(seller_uid).update({"status": status})


def add_product(seller_uid, seller_name, title, category, crop_target, price, description, image_url):
    db = get_db()
    db.collection("products").add({
        "sellerUid": seller_uid,
        "sellerName": seller_name,
        "title": title,
        "category": category,
        "cropTarget": crop_target,
        "price": price,
        "description": description,
        "imageUrl": image_url,
        "createdAt": firestore.SERVER_TIMESTAMP,
    })


def get_products_by_seller(seller_uid):
    db = get_db()
    docs = db.collection("products").where("sellerUid", "==", seller_uid).stream()
    products = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        products.append(data)
    return products


def get_all_products():
    db = get_db()
    docs = db.collection("products").stream()
    products = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        products.append(data)
    return products


def get_products_for_crop(crop_name):
    db = get_db()
    docs = db.collection("products").stream()
    products = []
    for doc in docs:
        data = doc.to_dict()
        target = (data.get("cropTarget") or "").lower()
        if not target or "all" in target or crop_name.lower() in target:
            data["id"] = doc.id
            products.append(data)
    return products
