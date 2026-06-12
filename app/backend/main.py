import json
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
import uvicorn
import tensorflow as tf
import numpy as np
from PIL import Image
import io

# Initialize the FastAPI application instance
app = FastAPI(title="plant doctor")

# --- 1. DYNAMIC FILE PATH PATH CONFIGURATIONS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Adjusting filenames to match your exact repository structure
MODEL_PATH = os.path.normpath(os.path.join(BASE_DIR, "trained_model", "plant_disease_diagnostics_CNN.h5"))
CLASSES_PATH = os.path.join(BASE_DIR, "class_indices.json")
TREATMENTS_PATH = os.path.join(BASE_DIR, "treatment_data.json")

# Diagnostics for the file existance
print("\n=== SYSTEM PATH CHECK ===")
print(f"BASE_DIR calculated as: {BASE_DIR}")
print(f"Looking for Model at:   {MODEL_PATH} -> Exists? {os.path.exists(MODEL_PATH)}")
print(f"Looking for Classes at: {CLASSES_PATH} -> Exists? {os.path.exists(CLASSES_PATH)}")
print(f"Looking for Treatments at: {TREATMENTS_PATH} -> Exists? {os.path.exists(TREATMENTS_PATH)}")
print("=========================\n")


# --- 2. LOAD COMPONENT RESOURCES AT SERVER STARTUP ---
try:
    # Load your trained Keras CNN h5 file
    model = tf.keras.models.load_model(MODEL_PATH)
    
    # Load mapping index dictionary configurations
    with open(CLASSES_PATH, "r") as f:
        class_indices = json.load(f)
        
    # Load treatment recommendations dictionary data
    with open(TREATMENTS_PATH, "r") as f:
        treatment_data = json.load(f)
        
    print("🚀 All ML models and treatment databases loaded successfully!")
except Exception as e:
    print(f"❌ Initialization Error: Ensure paths and filenames match perfectly. Details: {e}")
    model, class_indices, treatment_data = None, {}, {}


# --- 3. HELPER FUNCTION FOR IMAGE PREPROCESSING ---
def preprocess_image(image_bytes: bytes) -> np.ndarray:

    """Converts uploaded raw file bytes to normalized tensors matching CNN structure."""
    
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")  # From the frontend it fetches the file that was converted into bytes and it is opened here
    img = img.resize((224, 224))                              # Resize to your model's input size
    img_array = np.array(img).astype("float32") / 255.0       # Normalize pixel arrays
    img_array = np.expand_dims(img_array, axis=0)             # Expand to batch dimension shape: (1, 224, 224, 3)
    return img_array


# --- 4. API INFERENCE ENDPOINT ---
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Fallback gatekeeper validation check if loading failed
    if model is None:
        raise HTTPException(status_code=500, detail="Model file is missing or failed to initialize.")
        
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file stream type must be a valid image format.")

    try:
        # Read the asynchronous file upload stream
        contents = await file.read()
        processed_image = preprocess_image(contents)
        
        # Execute forward pass inference on your CNN
        predictions = model.predict(processed_image)
        class_index = str(np.argmax(predictions[0]))
        confidence = float(predictions[0].max()*100)
        
        # Step 1: Extract disease string flag from class_indices.json using prediction number index
        raw_disease_name = class_indices.get(class_index, "Unknown")
        
        # Normalize the string formatting into a snake_case key to securely access treatment_data.json keys
        lookup_key = raw_disease_name
        
        # Step 2: Fetch the complete dataset dictionary using the generated key flag lookup
        treatment = treatment_data.get(lookup_key, {
            "disease_name": raw_disease_name,
            "how_to_handle_infected_leaves": "No specific handling data found for this condition configuration.",
            "how_to_irrigate": "No specific field adjustments tracked.",
            "chemicals_for_treatment": "Consult an agricultural extension or expert.",
            "locally_available_chemicals_in_india": "N/A",
            "precautions_to_prevent_recurrence": "Monitor plant development closely.",
            "professional_consultation_disclaimer": "Verify with regional authorities."
        })
        
        # Step 3: Return the structured application payload back to the awaiting Streamlit layout
        return {
            "prediction_index": int(class_index),
            "disease": treatment.get("disease_name", raw_disease_name),
            "confidence": confidence,
            "treatment_details": treatment
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference Engine Internal Failure: {str(e)}")


@app.get("/")
def health_check():
    return {"status": "healthy", "service": "Plant diagnosis and treatment"}


if __name__ == "__main__":
    # Spins up your backend endpoint listener locally on port 8000
    uvicorn.run("main.py:app", host="127.0.0.1", port=8000, reload=True)