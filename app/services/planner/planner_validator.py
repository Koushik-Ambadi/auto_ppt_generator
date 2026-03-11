# app\services\planner\planner_validator.py
import os
import json
from jsonschema import Draft7Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT7

# =====================================================
# CONFIG
# =====================================================

SCHEMA_DIR = "schemas"
TEMPLATE_DIR = "templates_library/template_specs"

STRICT_MODE = True   # If False → auto-truncate instead of reject

# =====================================================
# BUILD REGISTRY (CORRECT + FUTURE-PROOF)
# =====================================================

def build_registry(schema_dir):
    registry = Registry()

    for filename in os.listdir(schema_dir):
        if filename.endswith(".json"):
            path = os.path.join(schema_dir, filename)

            with open(path, "r") as f:
                schema = json.load(f)

            # 🔑 MUST use $id for referencing to work
            schema_id = schema.get("$id")
            if not schema_id:
                raise ValueError(f"Schema '{filename}' is missing $id")

            registry = registry.with_resource(
                schema_id,
                Resource.from_contents(schema, default_specification=DRAFT7)
            )

    return registry


registry = build_registry(SCHEMA_DIR)

# =====================================================
# VALIDATOR (ROOT SCHEMA MUST COME FROM REGISTRY)
# =====================================================

ROOT_SCHEMA_ID = "presentation_plan.schema.json"

presentation_schema = registry.get(ROOT_SCHEMA_ID).contents

validator = Draft7Validator(
    presentation_schema,
    registry=registry
)

# =====================================================
# PASS 1 — SCHEMA VALIDATION
# =====================================================

def validate_schema(presentation_json):
    errors = sorted(validator.iter_errors(presentation_json), key=lambda e: e.path)

    if errors:
        return False, [
            f"{list(error.path)} → {error.message}"
            for error in errors
        ]

    return True, []

# =====================================================
# LOAD TEMPLATE CONTRACT
# =====================================================

def load_template_contract(template_id):
    path = os.path.join(TEMPLATE_DIR, f"{template_id}.json")
    if not os.path.exists(path):
        raise Exception(f"Template contract not found: {template_id}")
    with open(path, "r") as f:
        return json.load(f)

# =====================================================
# PASS 2 — TEMPLATE VALIDATION
# =====================================================

def enforce_text_limit(text, max_chars):
    if max_chars and len(text) > max_chars:
        return text[:max_chars]
    return text


def validate_template_constraints(presentation_json):
    errors = []
    warnings = []

    for slide_index, slide in enumerate(presentation_json["slides"]):
        template_id = slide["template_id"]
        content = slide["content"]

        template_contract = load_template_contract(template_id)
        placeholders = template_contract["placeholders"]

        # 1️⃣ Required placeholders
        for name, rules in placeholders.items():
            if not rules.get("optional", False) and name not in content:
                errors.append(
                    f"Slide {slide_index}: Missing required placeholder '{name}'"
                )

        # 2️⃣ Validate content fields
        for field, value in content.items():

            if field not in placeholders:
                errors.append(
                    f"Slide {slide_index}: Placeholder '{field}' not allowed in template '{template_id}'"
                )
                continue

            rules = placeholders[field]
            field_type = rules["type"]

            # TEXT
            if field_type == "text":
                if not isinstance(value, str):
                    errors.append(f"Slide {slide_index}: '{field}' must be string")
                    continue

                max_chars = rules.get("max_chars")
                if max_chars and len(value) > max_chars:
                    if STRICT_MODE:
                        errors.append(
                            f"Slide {slide_index}: '{field}' exceeds {max_chars} chars"
                        )
                    else:
                        content[field] = enforce_text_limit(value, max_chars)
                        warnings.append(
                            f"Slide {slide_index}: '{field}' truncated"
                        )

            # BULLETS
            elif field_type == "bullets":
                if not isinstance(value, list):
                    errors.append(f"Slide {slide_index}: '{field}' must be list")
                    continue

                max_items = rules.get("max_items")
                max_chars = rules.get("max_chars")

                if max_items and len(value) > max_items:
                    if STRICT_MODE:
                        errors.append(
                            f"Slide {slide_index}: '{field}' exceeds {max_items} bullets"
                        )
                    else:
                        content[field] = value[:max_items]
                        warnings.append(
                            f"Slide {slide_index}: bullet list truncated"
                        )

                for i, bullet in enumerate(value):
                    if max_chars and len(bullet) > max_chars:
                        if STRICT_MODE:
                            errors.append(
                                f"Slide {slide_index}: bullet {i} exceeds {max_chars} chars"
                            )
                        else:
                            content[field][i] = enforce_text_limit(bullet, max_chars)
                            warnings.append(
                                f"Slide {slide_index}: bullet {i} truncated"
                            )

            # IMAGE
            elif field_type == "image":
                if not template_contract.get("allowed_images", False):
                    errors.append(
                        f"Slide {slide_index}: images not allowed in template '{template_id}'"
                    )

            # CHART
            elif field_type == "chart":
                allowed_charts = template_contract.get("allowed_charts", [])
                chart_type = value.get("type")

                if chart_type not in allowed_charts:
                    errors.append(
                        f"Slide {slide_index}: chart type '{chart_type}' not allowed"
                    )

    return errors, warnings

# =====================================================
# MAIN VALIDATION PIPELINE
# =====================================================

def validate_presentation(presentation_json):

    # Pass 1 — schema validation
    schema_valid, schema_errors = validate_schema(presentation_json)
    if not schema_valid:
        return {
            "status": "rejected_schema",
            "errors": schema_errors
        }

    # Pass 2 — template validation
    template_errors, template_warnings = validate_template_constraints(presentation_json)

    if template_errors:
        return {
            "status": "rejected_template",
            "errors": template_errors,
            "warnings": template_warnings
        }

    return {
        "status": "valid",
        "warnings": template_warnings
    }
