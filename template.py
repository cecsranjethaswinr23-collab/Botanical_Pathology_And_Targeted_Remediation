import os
from pathlib import Path

project_name = "Plant_treatment_Analysis"

list_of_files = [
    "app/backend/main.py",           # FastAPI Backend
    "app/backend/class_indices.json",
    "app/backend/treatment_data.json",
    "app/frontend/ui.py",            # Streamlit UI
    "app/Dockerfile.backend",
    "app/Dockerfile.frontend",
    "docker-compose.yml",            # Links both containers
    "requirements.txt",              # Shared dependencies
    ".gitignore"                     # Prevents pushing junk to GitHub
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass

# Automatically populate the .gitignore file with python/ML defaults
gitignore_path = Path(".gitignore")
with open(gitignore_path, "w") as f:
    f.write(
        ".venv/\n"
        "__pycache__/\n"
        "*.pyc\n"
        ".ipynb_checkpoints/\n"
        ".DS_Store\n"
        # "app/backend/trained_model/*.h5\n" # Uncomment if you want to keep the model off GitHub
    )
print("Project structure and .gitignore generated successfully!")