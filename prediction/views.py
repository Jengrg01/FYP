from django.conf import settings
import os
import cv2
import gdown
import joblib
import dlib
import numpy as np
from django.core.files.storage import default_storage
from django.http import JsonResponse
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from django.views.decorators.csrf import csrf_exempt

# Store models in `src/ml_models/`
MODEL_DIR = os.path.join(settings.BASE_DIR, "ml_models")
os.makedirs(MODEL_DIR, exist_ok=True)

# Google Drive model links
MODEL_LINKS = {
    "face_model": "https://drive.google.com/uc?id=1srRaJbXwqKMrUVpkE5fUZSveRCdasgAS",
    "skin_model": "https://drive.google.com/uc?id=1-1XE7VxhRMdLyWONn8EK2cu8_xfrCqZg",
    "hybrid_model": "https://drive.google.com/uc?id=1-5VgKyLZLlNYK_9-vV7bdB86AAAbaTsX",
    "svm_classifier": "https://drive.google.com/uc?id=1QUYUn-VO8Vpqe6igUdcNdHH7oF_N8Bdg",
}

LANDMARK_MODEL_ID = "1GqGJ-PW7xCG_-L9x_PjMpMErdfNXlvGA"

def download_file_from_drive(file_id, dest_path):
    url = f"https://drive.google.com/uc?id={file_id}"
    if not os.path.exists(dest_path):  # Download only if not already present
        print(f"Downloading {os.path.basename(dest_path)}...")
        gdown.download(url, dest_path, quiet=False)

landmark_model_path = os.path.join(MODEL_DIR, "shape_predictor_68_face_landmarks.dat")
download_file_from_drive(LANDMARK_MODEL_ID, landmark_model_path)

# Function to download models
def download_model(filename, url):
    model_path = os.path.join(MODEL_DIR, filename)
    if not os.path.exists(model_path):
        print(f"Downloading {filename}...")
        gdown.download(url, model_path, quiet=False)
    return model_path

# Download & Load Models
face_model = load_model(download_model("faceshape_model.keras", MODEL_LINKS["face_model"]))
skin_model = load_model(download_model("skintone_model.keras", MODEL_LINKS["skin_model"]))
hybrid_model = load_model(download_model("hybrid_facial_features.keras", MODEL_LINKS["hybrid_model"]))
svm_classifier = joblib.load(download_model("makeup_classifier.pkl", MODEL_LINKS["svm_classifier"]))


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(landmark_model_path)

# Label Mappings
face_labels = ["Heart", "Oblong", "Oval", "Round", "Square"]
skin_labels = {0: "dark", 1: "light", 2: "mid-dark", 3: "mid-light"}
feature_labels = ["Small", "Medium", "Big"]
makeup_labels = ["Arabic Makeup", "Douyin Makeup", "Indian Makeup", "Japanese Makeup", "Korean Makeup", "Western Makeup"]

def preprocess_image(image_path):
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img) 
    img_array = np.expand_dims(img_array, axis=0)
    img_array /=255.0
    return img_array

# Model Prediction Functions
def predict_face_shape(image_path):
    try:
        processed_img = preprocess_image(image_path)
        prediction = face_model.predict(processed_img)
        return face_labels[np.argmax(prediction)]
    except Exception as e:
        print(f"Error in face prediction: {e}")
        return "Error"

def predict_skin_tone(image_path):
    processed_img = preprocess_image(image_path)
    prediction = skin_model.predict(processed_img)
    return skin_labels[np.argmax(prediction)]


@csrf_exempt
def upload_image(request):
    print("Received upload request")
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        image_path = default_storage.save(f"uploads/{image.name}", image)
        image_path = default_storage.path(image_path)
        if not os.path.exists(image_path):
            print(f"Image {image_path} was not saved correctly!")

        face_class = predict_face_shape(image_path)
        skin_class = predict_skin_tone(image_path)

        # Convert labels to numerical features
        skin_values = {"dark": 0, "light": 1, "mid-dark": 2, "mid-light": 3}
        face_values = {"Heart": 0, "Oblong": 1, "Oval": 2, "Round": 3, "Square": 4}
        feature_values = {"Small": 0, "Medium": 1, "Big": 2}


        # Clean up saved file
        os.remove(image_path)
        print("Returning face Response:", face_class)
        print("Returning skin Response:", skin_class)
        return JsonResponse({
            "face_shape": face_class,
            "skin_tone": skin_class,
        })

    return JsonResponse({"error": "No image uploaded"}, status=400)