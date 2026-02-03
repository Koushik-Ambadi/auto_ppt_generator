# services/ppt/text_renderer.py
def render_text(slide, placeholder_name, value):
    for shape in slide.shapes:
        if shape.name == placeholder_name:
            tf = shape.text_frame
            tf.clear()

            if isinstance(value, str):
                tf.text = value
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if i == 0:
                        tf.text = item
                    else:
                        p = tf.add_paragraph()
                        p.text = item
                        p.level = 1
            return
