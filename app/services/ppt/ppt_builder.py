from pptx import Presentation
from .slide_renderer import render_slide

def build_presentation(presentation_json, output_path):
    prs = Presentation("templates_library/ppt_templates/master_template.pptx")

    for slide_json in presentation_json["slides"]:
        render_slide(prs, slide_json)

    prs.save(output_path)
