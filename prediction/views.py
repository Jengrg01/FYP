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

AVG_EYE_SIZE = 15.0
AVG_LIP_THICKNESS = 8.0
AVG_NOSE_SIZE = 20.0

def preprocess_image(image_path):
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img) 
    img_array = np.expand_dims(img_array, axis=0)
    img_array /=255.0
    return img_array

def extract_facial_features(image_path):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(landmark_model_path)
    print(f"Loading image: {image_path}")

    img = cv2.imread(image_path)
    print(f"Image type: {type(img)}, Shape: {img.shape if img is not None else 'None'}")

    if img is None:
        print(f"Error: Could not load image {image_path}")
        return None

    if img.dtype != np.uint8:
        img = img.astype(np.uint8)


    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = gray.astype(np.uint8)

# Ensure it's contiguous in memory
    gray = np.ascontiguousarray(gray)

    if detector is None:
        print("Error: dlib detector not initialized properly.")


    if gray is None or len(gray.shape) != 2:  # Ensure it's a proper grayscale image
        raise RuntimeError("Invalid image format. Make sure the image is 8-bit grayscale or RGB.")

    # Debugging output
    print(f"Image converted to grayscale, Shape: {gray.shape}, Type: {gray.dtype}")

    faces = detector(gray)

    print(f"Faces detected: {len(faces)}")  # Debugging output


    if len(faces) == 0:
        raise RuntimeError("No face detected in the image")


    for face in faces:
        landmarks = predictor(gray, face)

        # Extract Features
        eye_size = np.linalg.norm([landmarks.part(42).x - landmarks.part(45).x])  # Eye width
        lip_thickness = np.linalg.norm([landmarks.part(62).y - landmarks.part(66).y])  # Lip thickness
        nose_size = np.linalg.norm([landmarks.part(31).x - landmarks.part(35).x])  # Nose width

        # Classify Features
        eye_class = "Big" if eye_size > AVG_EYE_SIZE else "Small"
        lip_class = "Thick" if lip_thickness > AVG_LIP_THICKNESS else "Thin"
        nose_class = "Big" if nose_size > AVG_NOSE_SIZE else "Small"

        return [eye_size, lip_thickness, nose_size, eye_class, lip_class, nose_class]
    return None  # If no faces are found



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
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    face_class = predict_face_shape(image_path)
    skin_class = predict_skin_tone(image_path)
    extracted_features = extract_facial_features(image_path)
    if extracted_features is None:
        return "No face detected"
    eye_size, lip_thickness, nose_size, eye_class, lip_class, nose_class = extracted_features
    extracted_features_array = np.array([[eye_size, lip_thickness, nose_size]])
    feature_pred = hybrid_model.predict([img_array, extracted_features_array])

    feature_class = ["Small", "Medium", "Big"][np.argmax(feature_pred)]

    return skin_class, face_class, eye_class, nose_class, lip_class

@csrf_exempt
def upload_image(request):
    print("Received upload request")
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        image_path = default_storage.save(f"uploads/{image.name}", image)
        image_path = default_storage.path(image_path)
        if not os.path.exists(image_path):
            print(f"Image {image_path} was not saved correctly!")

        results = predict_facial_features(image_path)
        if results is None:
            return "No face detected."

        skin_class, face_class, eye_class, nose_class, lip_class = results

    # Combine Predictions for SVM Model
        features_for_svm = np.array([[skin_labels.index(skin_class),
                                  face_labels.index(face_class),
                                  1 if eye_class == "Big" else 0,
                                  1 if nose_class == "Big" else 0,
                                  1 if lip_class == "Thick" else 0]])

    
        makeup_pred = svm_classifier.predict(features_for_svm)
        final_makeup = makeup_labels[makeup_pred[0]]
        # Clean up saved file
        os.remove(image_path)
        print(f"Skin Tone: {skin_class}, Face Shape: {face_class}, Features: {eye_class}, {nose_class}, {lip_class}")
        print(f"Best Makeup Recommendation: {final_makeup}")
        return JsonResponse({
            "face_shape": face_class,
            "skin_tone": skin_class,
            "eye_class" : eye_class,
        })

    return JsonResponse({"error": "No image uploaded"}, status=400)