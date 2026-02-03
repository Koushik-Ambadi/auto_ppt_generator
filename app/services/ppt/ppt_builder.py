# services/ppt/ppt_builder.py
from pptx import Presentation
from .slide_renderer import render_slide

def build_presentation(presentation_json, output_path):
    """Build a presentation from JSON using POTX templates."""

    prs = Presentation()  # empty presentation

    for slide_json in presentation_json["slides"]:
        render_slide(prs, slide_json)

    prs.save(output_path)
    return output_path
