# 🍅 Botanical Pathology And Targeted Remediation System

An end-to-end, production-ready Deep Learning pipeline that classifies plant diseases and provides localized, actionable treatment protocols for farmers and people grow plants in their garden, balcony, etc... .This project specifically trained on ten tomato plant diseases is This project demonstrates real-time image inference, and secure automated deployment.

---

## 📱 Project Application Screenshots

### 1. User Interface & Image Analysis
*The web interface allows users to upload leaf images, leveraging a CNN model for instant, high-accuracy disease diagnosis.*
<img width="1905" height="885" alt="plant doc Dashboard" src="https://github.com/user-attachments/assets/38ec35f0-5c71-4170-a030-41c6f08b75ad" />


### 2. Treatment & Professional Guidance
*Diagnostic results provide immediate, localized chemical treatment recommendations (Indian Market) and professional safety protocols.*
<img width="977" height="797" alt="plant doc result 1" src="https://github.com/user-attachments/assets/2efe7689-88d8-4b3c-bdc2-4485752b0b5a" />
<img width="942" height="717" alt="plant doc result 2" src="https://github.com/user-attachments/assets/f4ced19a-b572-4d30-9703-ce4dea777ada" />

---

## 🛠️ Tech Stack & Tools

**Language:** Python
**Deep Learning:** TensorFlow, OpenCV (Image Preprocessing)
**API & Backend:** FastAPI
**Cloud Deployment:** Docker, AWS (EC2![Uploading plant doc Dashboard.jpg…]()
)
**Frontend:** Streamlit

---

## 🚀 Key Features

**Localized Remediation Data:** Outputs chemical treatments mapped specifically to trade names widely available in India.
**Best-Practice Advisory:** Dynamically generates irrigation and hygiene protocols tailored to the diagnosed pathogen to prevent secondary spread.
**Secure Microservices Architecture:** Decoupled Frontend and Backend services orchestrated via Docker Compose for high availability and scalability.
---

## 📐 Architecture & Pipeline Flow

```text
 ┌─────────────────┐      ┌──────────────────┐      ┌──────────────────────┐
 │   User Input    ├─────►│  FastAPI Backend ├─────►│  CNN Inference Engine│
 │  (Image Upload) │      │  (Data Mapping)  │      │  (.h5 / SavedModel)  │
 └─────────────────┘      └──────────────────┘      └──────────┬───────────┘
                                                               │
 ┌─────────────────┐      ┌──────────────────┐      ┌──────────▼───────────┐
 │   Result View   │◄─────┤ Treatment Lookup ├◄─────┤  Diagnosis Output    │
 │ (Actionable Data)      │ (Indian Market DB)      │ (Probability Score)  │
 └─────────────────┘      └──────────────────┘      └──────────────────────┘

 ## Project Links & Author

**Repository:** [GitHub](https://github.com/cecsranjethaswinr23-collab/Botanical_Pathology_And_Targeted_Remediation)
**Author:** Ranjeth Aswin Ravindran
**Connect with me:** 👋 [LinkedIn](www.linkedin.com/in/ranjeth-aswin-ravindran-018277253)
                         [GitHub](https://github.com/cecsranjethaswinr23-collab)
