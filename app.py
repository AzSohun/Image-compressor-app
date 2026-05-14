from PIL import Image
import os
import gradio as gr
from io import BytesIO

def compress_image(image_input, output_filename, quality):
    if image_input is None:
        return None, "Please upload your image."

    output_filename = str(output_filename)
    quality = int(quality)

    if "." not in output_filename:
        output_filename += ".jpg"

    image = Image.open(image_input)

    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    max_width = 1280
    max_height = 1280
    image.thumbnail((max_width, max_height))

    output_buffer = BytesIO()
    image.save(output_buffer, format=image.format if image.format else "JPEG", optimize=True, quality=quality)
    output_buffer.seek(0)

    new_size = len(output_buffer.getvalue()) / 1024
    message = f"Reduced Size: {new_size: .2f} KB"

    return output_buffer.getvalue(), message

iface = gr.Interface(
    fn=compress_image,
    inputs=[
        gr.Image(type="file", label="Upload Image"),
        gr.Textbox(label="Output Filename (e.g., compressed_image.jpg)", value="compressed_image.jpg"),
        gr.Slider(minimum=1, maximum=100, value=75, label="Image Quality (1-100)")
    ],
    outputs=[
        gr.File(label="Download Compressed Image"),
        gr.Textbox(label="Compression Info")
    ],
    title="Image Compressor",
    description="Upload an image, choose an output filename and quality, and download the compressed version."
)

iface.launch(debug=True)