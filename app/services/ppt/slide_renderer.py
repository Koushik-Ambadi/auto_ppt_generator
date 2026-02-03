# services/ppt/slide_renderer.py
import os
from pptx import Presentation
from .text_renderer import render_text
from .chart_renderer import render_chart
from .image_renderer import render_image

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, "templates_library", "ppt_templates")


def get_template(template_id):
    """Load POTX template as a Presentation object."""
    template_path = os.path.join(TEMPLATE_DIR, f"{template_id}.pptx")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found: {template_path}")
    return Presentation(template_path)


def render_slide(prs, slide_json):
    """
    Add a new slide to `prs` using the template specified in slide_json,
    and populate placeholders with content.
    """
    template_id = slide_json["template_id"]
    content = slide_json["content"]

    # Load the template
    template_prs = get_template(template_id)

    # Use the first slide layout from the template (or choose by index)
    slide_layout = template_prs.slide_layouts[0]  

    # Add new slide to the main presentation
    slide = prs.slides.add_slide(slide_layout)

    # Fill placeholders safely
    for placeholder_name, value in content.items():
        # Try to render text
        render_text(slide, placeholder_name, value)

        # Render charts if applicable
        if isinstance(value, dict) and value.get("type"):
            render_chart(slide, placeholder_name, value)

        # Render images if applicable
        if isinstance(value, dict) and value.get("description"):
            render_image(slide, placeholder_name, value)
