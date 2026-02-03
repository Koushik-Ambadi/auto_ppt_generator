from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.enum.shapes import PP_PLACEHOLDER
import json
import os

# -----------------------------
# Placeholder → semantic field
# -----------------------------

PLACEHOLDER_FIELD_MAP = {
    PP_PLACEHOLDER.TITLE: "title",
    PP_PLACEHOLDER.CENTER_TITLE: "title",
    PP_PLACEHOLDER.SUBTITLE: "subtitle",
    PP_PLACEHOLDER.BODY: "bullets",
    PP_PLACEHOLDER.OBJECT: "content",
    PP_PLACEHOLDER.PICTURE: "image",
    PP_PLACEHOLDER.CHART: "chart",
    PP_PLACEHOLDER.TABLE: "table",
    PP_PLACEHOLDER.FOOTER: "footnote"
}

def placeholder_has_bullets(ph):
    if not hasattr(ph, "text_frame") or not ph.text_frame:
        return False

    for p in ph.text_frame.paragraphs:
        if p.level > 0 or p.font.size is None:
            return True
    return False


def infer_field_type(placeholder_type):
    if placeholder_type in (
        PP_PLACEHOLDER.TITLE,
        PP_PLACEHOLDER.CENTER_TITLE,
        PP_PLACEHOLDER.SUBTITLE,
        PP_PLACEHOLDER.FOOTER
    ):
        return "text"
    if placeholder_type == PP_PLACEHOLDER.BODY:
        return "bullets"
    if placeholder_type == PP_PLACEHOLDER.PICTURE:
        return "image"
    if placeholder_type == PP_PLACEHOLDER.CHART:
        return "chart"
    if placeholder_type == PP_PLACEHOLDER.TABLE:
        return "table"
    return "text"

# -----------------------------
# Schema extraction
# -----------------------------

def extract_template_schema(ppt_path):
    prs = Presentation(ppt_path)
    template_id = os.path.splitext(os.path.basename(ppt_path))[0]

    schema = {
        "template_id": template_id,
        "description": "",
        "slides": []
    }

    content_types_seen = set()

    for slide_idx, slide in enumerate(prs.slides, start=1):
        slide_schema = {
            "slide_index": slide_idx,
            "fields": {}
        }

        for ph in slide.placeholders:
            ph_type = ph.placeholder_format.type
            field_name = PLACEHOLDER_FIELD_MAP.get(
                ph_type, f"field_{ph.placeholder_format.idx}"
            )

            # Ensure unique field names
            original_name = field_name
            counter = 2
            while field_name in slide_schema["fields"]:
                field_name = f"{original_name}_{counter}"
                counter += 1

            # Infer bullets vs text for BODY placeholders
            if ph_type == PP_PLACEHOLDER.BODY and placeholder_has_bullets(ph):
                field_type = "bullets"
            else:
                field_type = infer_field_type(ph_type)
            content_types_seen.add(field_type)

            slide_schema["fields"][field_name] = {
                "type": field_type,
                "placeholder_index": ph.placeholder_format.idx
            }

        schema["slides"].append(slide_schema)

    # -----------------------------
    # Auto description (LLM hint)
    # -----------------------------

    if "chart" in content_types_seen:
        schema["description"] = (
            "Template with chart placeholders for presenting structured data and metrics."
        )
    elif "image" in content_types_seen:
        schema["description"] = (
            "Visual-focused template combining images with supporting text."
        )
    elif "bullets" in content_types_seen:
        schema["description"] = (
            "Text-driven template suitable for summaries, bullet points, and explanations."
        )
    else:
        schema["description"] = "General-purpose presentation template."

    return schema

# -----------------------------
# Main runner
# -----------------------------

if __name__ == "__main__":
    INPUT_DIR = "templates_library/ppt_templates"
    OUTPUT_DIR = "templates_library/template_specs"

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not os.path.isdir(INPUT_DIR):
        raise FileNotFoundError(f"Directory not found: {INPUT_DIR}")

    for file_name in os.listdir(INPUT_DIR):
        if not file_name.lower().endswith(".pptx"):
            continue

        ppt_path = os.path.join(INPUT_DIR, file_name)
        schema = extract_template_schema(ppt_path)

        output_path = os.path.join(
            OUTPUT_DIR, f"{schema['template_id']}.json"
        )

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(schema, f, indent=2)

        print(f"Generated schema → {output_path}")
