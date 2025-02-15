import os
import cv2
import mediapipe as mp
import numpy as np
import pymongo
import pickle
import bcrypt
from PIL import Image

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["AivaDB"]
users_collection = db["users"]

mp_face_mesh = mp.solutions.face_mesh


def facelandmarks(image_array):
    with mp_face_mesh.FaceMesh(static_image_mode=True, refine_landmarks=True) as face_mesh:
        results = face_mesh.process(image_array)
        if not results.multi_face_landmarks:
            return None
        return np.array(
            [[lm.x, lm.y, lm.z] for lm in results.multi_face_landmarks[0].landmark]
        ).flatten()


def facelandmarksimg(image_path):
    image_path = image_path.strip().strip('"')
    if not os.path.exists(image_path):
        return None
    img = Image.open(image_path).convert('RGB')
    img_array = np.array(img)
    return facelandmarks(img_array)


def captureface():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return None
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        cv2.imshow("Face Capture - Press SPACE to capture", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 32:
            break
    cap.release()
    cv2.destroyAllWindows()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return facelandmarks(frame_rgb)


def register(user, pwd, imgpath):
    if users_collection.find_one({"username": user}):
        return "Username already exists. Choose another."
    hashed_pwd = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())
    face_data = facelandmarksimg(imgpath)
    if face_data is None:
        return "No face detected. Try another image."
    users_collection.insert_one({
        "username": user,
        "password": hashed_pwd,
        "face_encoding": pickle.dumps(face_data)
    })
    return "Signup successful! Face authentication enabled."


def faceverify(stored_data):
    stored_data = pickle.loads(stored_data)
    live_data = captureface()
    if live_data is None:
        return False
    return np.allclose(stored_data, live_data, atol=0.05)


def signin(user, pwd):
    user_data = users_collection.find_one({"username": user})
    if not user_data:
        return "User not found."
    if not bcrypt.checkpw(pwd.encode(), user_data["password"]):
        return "Incorrect password."
    if faceverify(user_data["face_encoding"]):
        return f"Login successful. Welcome, {user}!"
    else:
        return "Face authentication failed. Access denied."
