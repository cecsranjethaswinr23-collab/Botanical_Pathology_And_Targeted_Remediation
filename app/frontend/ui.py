import streamlit as st
import requests
from PIL import Image
import io

# Set up page configurations
st.set_page_config(
    page_title="plant doctor",
    page_icon="👨‍⚕️",
    layout="centered"
)

# ABOUt sidebar
st.sidebar.title("About")
st.sidebar.markdown("""
### 🎯 WHAT IT DOES:
This Deep Learning application specializes in high-accuracy image recognition. 
Using a custom-trained **Convolutional Neural Network (CNN)**, it automates the 
process of identifying and classifying complex visual data in seconds. This application 
is made to get the immediate treatment for the plants right on the field to minimize 
the need of geting advices and diagnosis from various resources, where in that time the infections in 
the plants can be treated with various remedies the model gives like how to treat the infected 
leaves, irrigation, pesticides to use and so. This reduces the time to treat the plants, decrease 
the spread of infections and helps in increasing the yield.
""")
st.sidebar.subheader("🛠️ Tech Stack")
tech_stack = [
    "Python",
    "TensorFlow",
    "FastAPI",
    "Streamlit",
    "OpenCV",
    "NumPy & Pandas",
    "etc.."
]
for tech in tech_stack:
    st.sidebar.markdown(f"- **{tech}**")

st.sidebar.subheader("🔗 Source Code")
st.sidebar.link_button("💻 Go to GitHub Repository", "https://github.com/cecsranjethaswinr23-collab/Botanical_Pathology_And_Targeted_Remediation", use_container_width=True)

st.sidebar.markdown("### 👨‍💻 Developed By")
st.sidebar.markdown("**Ranjeth Aswin Ravindran**")
st.sidebar.caption("Data Scientist")

# Email bar
st.sidebar.markdown("""
📧 **Contact:** cecsranjethaswinr23@gmail.com
""")
# --------------------------#


# --- 1. TITLE & DESCRIPTION ---
st.title("Botanical Pathology and Remediation System 🌿")
st.markdown("""
Upload a image of a 🍅tomato plant's leaf below. A trained CNN 
model specifically tailored for diseases in tomato plants will analyze it via our FastAPI backend and return immediate localized treatment recommendations.
""")

st.write("---")


# --- 2. CONFIGURATION ---
# Points to your local FastAPI backend server instance
BACKEND_URL = "http://127.0.0.1:8000/predict"

# --- 3. IMAGE UPLOADER WIDGET ---
uploaded_file = st.file_uploader(
    "Choose a tomato plant leaf image...(only 🪴.jpg)", 
    type=["jpg"]
)

if uploaded_file is not None:
    # Read and display the image to the user instantly
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Sample Leaf Image", width=400)
    
    st.write("---")
    
    # Add a prominent analysis trigger button
    if st.button("🔍 Predict", type="primary"):
        with st.spinner("Uploading image to inference backend and analyzing..."):
            try:
                # Convert the uploaded file into raw bytes to transfer over HTTP
                img_bytes = io.BytesIO()
                image.save(img_bytes, format=image.format if image.format else "JPEG")
                img_bytes = img_bytes.getvalue()
                
                # Format payload payload structure for FastAPI's UploadFile
                files = {"file": (uploaded_file.name, img_bytes, uploaded_file.type)}
                
                # Send POST request to FastAPI server
                response = requests.post(BACKEND_URL, files=files, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Extract elements returned by backend dictionary logic
                    disease_name = result.get("disease", "Unknown Condition")
                    details = result.get("treatment_details", {})
                    confi = result.get("confidence")
                    
                    # --- 4. DISPLAY DIAGNOSIS RESULTS ---
                    st.success(f"### Diagnosis Result: **{disease_name}** with {confi:.2f}% confidense rate.")
                    
                    st.markdown("### 📋 Recommended Treatment & Action Plan")
                    
                    # Render your custom dictionary text blocks elegantly inside expander cards
                    with st.expander("✂️ How to Handle Infected Leaves", expanded=True):
                        st.write(details.get("how_to_handle_infected_leaves", "N/A"))
                        
                    with st.expander("💧 Irrigation adjustments", expanded=True):
                        st.write(details.get("how_to_irrigate", "N/A"))
                        
                    with st.expander("🧪 Chemical Treatment Options", expanded=True):
                        st.write(details.get("chemicals_for_treatment", "N/A"))
                        
                    with st.expander("🇮🇳 Locally Available Options (India)", expanded=True):
                        st.info(details.get("locally_available_chemicals_in_india", "N/A"))
                        
                    with st.expander("🛡️ Long-term Recurrence Prevention", expanded=False):
                        st.write(details.get("precautions_to_prevent_recurrence", "N/A"))
                        
                    # Noticeable disclaimer footer box
                    st.warning(f"⚠️ **Disclaimer:** {details.get('professional_consultation_disclaimer')}")
                    
                else:
                    # Handle backend error responses gracefully
                    error_detail = response.json().get('detail', 'Unknown backend error occurred.')
                    st.error(f"Backend Server Error ({response.status_code}): {error_detail}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection Failed: Could not connect to the FastAPI backend server. Make sure your backend terminal is running on port 8000.")
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {str(e)}")