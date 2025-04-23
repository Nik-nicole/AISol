# user_Service.py
from models.user import User
from app import bcrypt, Config, db
from Services.base_service import BaseService
import tensorflow as tf
import numpy as np
import cv2
import mediapipe as mp
import base64
import io
from PIL import Image


mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(min_detection_confidence=0.10, min_tracking_confidence=0.10)

# Load your trained model
model_path = "/home/fabrica/Desktop/IA LSC/AISol/prueba5.h5"
model = tf.keras.models.load_model(model_path)




# Define your actions
actions = np.array(['Hola', 'Gracias', 'Amor'])  # Replace with your actual signs

# Function to process MediaPipe results
def mediapipe_detection(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = holistic.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results

# Function to extract keypoints
def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])

class UserService(BaseService):
    def __init__(self):
        super().__init__(User)
    
    def create_user(self, user, from_google=False):
        # Validación de username y email
        if not user.username or not user.email:
            raise ValueError("Username and email are required")

        # Verificar si el email ya existe
        if self.model.query.filter_by(email=user.email).first():
            raise ValueError("Email is already registered")

        if from_google:
            # Usuario de Google: no exigimos password
            if user.password_hash is None or user.password_hash == "":
                user.password_hash = ""  # Se permite vacío
        else:
            # Registro local: sí exigimos password
            if not user.password_hash:
                raise ValueError("Password is required for local users")
            if len(user.password_hash) < Config.PASSWORD_MIN_LENGTH:
                raise ValueError(
                    f"Password must be at least {Config.PASSWORD_MIN_LENGTH} characters long"
                )
            # Encripta la contraseña
            user.password_hash = bcrypt.generate_password_hash(
                user.password_hash
            ).decode("utf-8", "ignore")

        return self.save(user)

    def authenticate_user(self, email, password):
        if not email or not password:
            raise ValueError("Email and password are required")
        user = self.model.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            return user
        return None

    def get_user_by_email(self, email):
        if not email:
            raise ValueError("Email is required")
        return self.model.query.filter_by(email=email).first()

    def get_user_by_id(self, user_id):
        if not user_id:
            raise ValueError("id is required")
        return self.model.query.get(user_id)
