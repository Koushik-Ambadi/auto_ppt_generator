# ==========================================
# CONFIGURE YOUR SCHEMA OUTPUT DIRECTORY
# ==========================================
base_path = "schemas"

import os
import json

os.makedirs(base_path, exist_ok=True)

# ==========================================
# CHART SCHEMA
# ==========================================

chart_schema = {
    "$id": "chart.schema.json",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Chart Schema",
    "type": "object",
    "required": ["type", "data"],
    "properties": {
        "type": {
            "type": "string",
            "enum": ["bar", "line", "pie"]
        },
        "data": {
            "type": "object",
            "required": ["labels", "values"],
            "properties": {
                "labels": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "values": {
                    "type": "array",
                    "items": {"type": "number"}
                }
            }
        },
        "title": {
            "type": "string"
        }
    },
    "additionalProperties": False
}

# ==========================================
# IMAGE SCHEMA
# ==========================================

image_schema = {
    "$id": "image.schema.json",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Image Schema",
    "type": "object",
    "required": ["description"],
    "properties": {
        "description": {"type": "string"},
        "source": {"type": "string"},
        "alt_text": {"type": "string"}
    },
    "additionalProperties": False
}

# ==========================================
# SLIDE SCHEMA
# ==========================================

slide_schema = {
    "$id": "slide.schema.json",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Slide Schema",
    "type": "object",
    "required": ["template_id", "content"],
    "properties": {
        "template_id": {
            "type": "string"
        },
        "content": {
            "type": "object",
            "additionalProperties": {
                "oneOf": [
                    {"type": "string"},
                    {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    {"$ref": "chart.schema.json"},
                    {"$ref": "image.schema.json"}
                ]
            }
        }
    },
    "additionalProperties": False
}

# ==========================================
# PRESENTATION PLAN SCHEMA
# ==========================================

presentation_schema = {
    "$id": "presentation_plan.schema.json",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Presentation Plan Schema",
    "type": "object",
    "required": ["presentation_title", "slides"],
    "properties": {
        "presentation_title": {
            "type": "string"
        },
        "slides": {
            "type": "array",
            "items": {"$ref": "slide.schema.json"}
        }
    },
    "additionalProperties": False
}

# ==========================================
# SAVE ALL SCHEMAS
# ==========================================

schemas = {
    "chart.schema.json": chart_schema,
    "image.schema.json": image_schema,
    "slide.schema.json": slide_schema,
    "presentation_plan.schema.json": presentation_schema
}

for filename, schema in schemas.items():
    path = os.path.join(base_path, filename)
    with open(path, "w") as f:
        json.dump(schema, f, indent=2)

print(f"Schemas saved in: {base_path}")
