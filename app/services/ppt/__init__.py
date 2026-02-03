# PPT package initializer: exposes all main functions from submodules

# Builder
from .ppt_builder import build_presentation

# Slide coordination
from .slide_renderer import render_slide

# Content renderers
from .text_renderer import render_text
from .chart_renderer import render_chart
from .image_renderer import render_image

# Optional: __all__ for cleaner imports
__all__ = [
    "build_presentation",
    "render_slide",
    "render_text",
    "render_chart",
    "render_image"
]
