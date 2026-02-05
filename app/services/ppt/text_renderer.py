def render_text(shape, value):
    """Render text or bullets into a given placeholder shape"""
    if not hasattr(shape, "text_frame"):
        return

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
