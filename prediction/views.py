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

AVG_EYE_SIZE = 15.0
AVG_LIP_THICKNESS = 8.0
AVG_NOSE_SIZE = 20.0

def extract_facial_features(image_path):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(landmark_model_path)

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found or unable to read")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    if len(faces) == 0:
        raise RuntimeError("No face detected in the image")

    face = faces[0]  # Assume one face per image
    landmarks = predictor(gray, face)

    # Extract Features
    eye_size = np.linalg.norm([landmarks.part(42).x - landmarks.part(45).x])  # Eye width
    lip_thickness = np.linalg.norm([landmarks.part(62).y - landmarks.part(66).y])  # Lip thickness
    nose_size = np.linalg.norm([landmarks.part(30).y - landmarks.part(33).y])  # Nose height

    # **Normalize and classify features (convert to 0 or 1)**
    eye_class = 1 if eye_size > AVG_EYE_SIZE else 0
    lip_class = 1 if lip_thickness > AVG_LIP_THICKNESS else 0
    nose_class = 1 if nose_size > AVG_NOSE_SIZE else 0

    return np.array([eye_class, lip_class, nose_class])  # Ensure output matches SVM input




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

def predict_facial_features(image_path):
    extracted_features = extract_facial_features(image_path)
    if extracted_features is None:
        return "No face detected"
    image = cv2.imread(image_path)  # Read the image
    image = cv2.resize(image, (224, 224))  # Resize to match model input shape
    image = image.astype(np.float32) / 255.0  # Normalize
    image = np.expand_dims(image, axis=0)  # Add batch dimension

    features = np.expand_dims(extracted_features, axis=0)

    prediction = hybrid_model.predict([image, features])
    return feature_labels[np.argmax(prediction)]


@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        image_path = default_storage.save(f"uploads/{image.name}", image)
        image_path = default_storage.path(image_path)

        try:
            # Get model predictions
            skin_class = predict_skin_tone(image_path)
            face_class = predict_face_shape(image_path)
            extracted_features = extract_facial_features(image_path)  # Get classified 0/1 values

            # Validate feature extraction
            if extracted_features is None or len(extracted_features) != 3:
                return JsonResponse({"error": "Facial features extraction failed"}, status=400)

            # Convert labels to numerical values for SVM input
            skin_values = {"dark": 0, "light": 1, "mid-dark": 2, "mid-light": 3}
            face_values = {"Heart": 0, "Oblong": 1, "Oval": 2, "Round": 3, "Square": 4}

            skin_val = skin_values.get(skin_class, -1)
            face_val = face_values.get(face_class, -1)

            # Ensure all features are valid
            if -1 in (skin_val, face_val):
                return JsonResponse({"error": "Invalid classification results"}, status=400)

            # Prepare features for SVM (Correct 5 features: skin, face, eye_class, nose_class, lip_class)
            features_for_svm = np.array([[skin_val, face_val, extracted_features[0], extracted_features[1], extracted_features[2]]])

            # Predict makeup style
            makeup_pred = svm_classifier.predict(features_for_svm)
            final_makeup = makeup_labels[makeup_pred[0]]

            # Clean up uploaded image
            os.remove(image_path)

            # Debug logs
            print(f"Skin Tone: {skin_class} -> {skin_val}")
            print(f"Face Shape: {face_class} -> {face_val}")
            print(f"Extracted Features (Binary): {extracted_features}")  # Should now be 0/1
            print(f"Predicted Makeup: {final_makeup}")

            return JsonResponse({
                "face_shape": face_class,
                "skin_tone": skin_class,
                "facial_features": {
                    "eye_size": "Big" if extracted_features[0] == 1 else "Small",
                    "lip_thickness": "Thick" if extracted_features[1] == 1 else "Thin",
                    "nose_size": "Big" if extracted_features[2] == 1 else "Small",
                },
                "recommended_makeup": final_makeup
            })

        except Exception as e:
            print(f"Error during processing: {e}")
            return JsonResponse({"error": "Internal server error"}, status=500)

    return JsonResponse({"error": "No image uploaded"}, status=400)
