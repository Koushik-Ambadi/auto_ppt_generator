# =============================
# CONFIGURE YOUR BASE FOLDER HERE
# =============================
base_path = "templates_library\\template_specs"   # <-- Change this to your desired folder path

import os
import json

# Create folder if it doesn't exist
os.makedirs(base_path, exist_ok=True)

# =============================
# TEMPLATE JSON DEFINITIONS
# =============================

templates = {
    "TEMPLATE_TITLE_V1.json": {
        "template_id": "TEMPLATE_TITLE_V1",
        "description": "Dark background title slide with subtitle",
        "placeholders": {
            "title": {"type": "text", "max_chars": 80, "optional": False},
            "subtitle": {"type": "text", "max_chars": 120, "optional": True}
        },
        "allowed_charts": [],
        "allowed_images": False
    },

    "TEMPLATE_EXEC_SUMMARY_V1.json": {
        "template_id": "TEMPLATE_EXEC_SUMMARY_V1",
        "description": "Executive summary slide with title and bullet list",
        "placeholders": {
            "title": {"type": "text", "max_chars": 70, "optional": False},
            "bullets": {
                "type": "bullets",
                "max_items": 5,
                "max_chars": 120,
                "optional": False
            }
        },
        "allowed_charts": [],
        "allowed_images": False
    },

    "TEMPLATE_TWO_COLUMN_V1.json": {
        "template_id": "TEMPLATE_TWO_COLUMN_V1",
        "description": "Two-column slide with text on left and image on right",
        "placeholders": {
            "title": {"type": "text", "max_chars": 70, "optional": False},
            "left_column": {
                "type": "bullets",
                "max_items": 4,
                "max_chars": 100,
                "optional": False
            },
            "right_content": {
                "type": "image",
                "max_items": 1,
                "optional": True
            }
        },
        "allowed_charts": [],
        "allowed_images": True
    },

    "TEMPLATE_CHART_V1.json": {
        "template_id": "TEMPLATE_CHART_V1",
        "description": "Data visualization slide with title, chart, and optional footnote",
        "placeholders": {
            "title": {"type": "text", "max_chars": 70, "optional": False},
            "chart": {"type": "chart", "optional": False},
            "footnote": {"type": "text", "max_chars": 150, "optional": True}
        },
        "allowed_charts": ["bar", "line", "pie"],
        "allowed_images": False
    },

    "TEMPLATE_IMAGE_V1.json": {
        "template_id": "TEMPLATE_IMAGE_V1",
        "description": "Image-focused slide with title and caption",
        "placeholders": {
            "title": {"type": "text", "max_chars": 70, "optional": False},
            "image": {
                "type": "image",
                "max_items": 1,
                "optional": False
            },
            "caption": {"type": "text", "max_chars": 120, "optional": True}
        },
        "allowed_charts": [],
        "allowed_images": True
    }
}

# =============================
# WRITE FILES
# =============================

for filename, content in templates.items():
    file_path = os.path.join(base_path, filename)
    with open(file_path, "w") as f:
        json.dump(content, f, indent=2)

print(f"All template JSON files saved to: {base_path}")
