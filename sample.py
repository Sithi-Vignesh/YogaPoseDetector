from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input
import numpy as np
import os

# --- Configuration ---
# Load the new trained model
MODEL_PATH = 'C:\\Users\\sithi\\Coding\\Yoga Hackathon\\YogaPoseDetection.keras'

# Define class labels (update these based on your training folders)
CLASS_LABELS = ['downdog', 'goddess', 'plank', 'tree', 'warrior2']

# --- Prediction Logic ---

def predict_image(model, img_path):
    """
    Loads an image, preprocesses it, and predicts using the loaded model.
    Prints the prediction and confidence score.

    Args:
        model: The loaded Keras model.
        img_path (str): The path to the image file.
    """
    try:
        # Load and preprocess the image
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        # Predict
        preds = model.predict(x)
        predicted_class_index = np.argmax(preds, axis=1)[0]
        confidence = np.max(preds)

        print(f"\n🩺 Prediction: {CLASS_LABELS[predicted_class_index]}")
        print(f"🔍 Confidence: {confidence:.2f}")

    except Exception as e:
        print(f"❌ Error processing image: {e}")

# --- Main Execution ---

if __name__ == "__main__":
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Error: Model file not found at '{MODEL_PATH}'")
        print("Please ensure the model file is in the correct directory.")
    else:
        print(f"✅ Model '{MODEL_PATH}' loaded successfully.")
        model = load_model(MODEL_PATH)

        while True:
            img_path_input = input("\n📁 Enter the full path to an eye image (or 'q' to quit): ").strip()

            if img_path_input.lower() == 'q':
                print("👋 Exiting program.")
                break

            if os.path.exists(img_path_input):
                predict_image(model, img_path_input)
            else:
                print("❌ File not found. Please check the path and try again.")