import json
import os
import sys

# Ensure 'app' folder is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # app/
sys.path.append(BASE_DIR)

from services.ppt.ppt_builder import build_presentation

# Paths
json_path = os.path.join(BASE_DIR, "services", "planner", "dummy_valid.json")
output_path = os.path.join(BASE_DIR, "storage", "outputs", "ppt", "dummy_valid.pptx")

# Ensure output folder exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Load JSON plan
with open(json_path, "r", encoding="utf-8") as f:
    presentation_json = json.load(f)

# Build presentation
build_presentation(presentation_json, output_path)

print(f"Presentation saved to {output_path}")
