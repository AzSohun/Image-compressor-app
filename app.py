from PIL import Image
import os
import gradio as gr
import tempfile # For creating temporary files

# This is your main function that will be called by Gradio
def compress_image(image_input_filepath, output_filename_str, quality):
    # Initialize variables for output
    output_filepath = None
    message = "Processing failed."
    temp_dir = None # To store the temporary directory path

    try:
        # 1. Input Validation
        # image_input_filepath will be a string (the path to the uploaded temporary file)
        if image_input_filepath is None:
            message = "Please upload your image."
            return output_filepath, message # Return None for file, error message for textbox

        # Ensure output_filename and quality are of the correct type
        output_filename = str(output_filename_str)
        quality = int(quality)

        # 2. Add a default file extension if missing, or use extension from desired output_filename
        if "." not in output_filename:
            output_filename += ".jpg" # Default to JPG if no extension provided

        # 3. Open the image using Pillow from the provided filepath
        image = Image.open(image_input_filepath)

        # 4. Convert image mode if necessary (e.g., RGBA to RGB for JPEG saving)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        # 5. Resize image (thumbnail maintains aspect ratio)
        max_width = 1280
        max_height = 1280
        image.thumbnail((max_width, max_height))

        # 6. Save the processed image to a TEMPORARY FILE with the desired output_filename
        # Gradio expects a filepath for gr.File when part of multiple outputs.
        # We create a temporary directory and save the file with the user-specified name inside it.
        temp_dir = tempfile.mkdtemp() # Create a unique temporary directory
        
        # Construct the full path for the temporary file using the desired output_filename
        # This path will be returned by the function.
        temp_output_path = os.path.join(temp_dir, output_filename)

        # Determine the format for Pillow save based on the desired output_filename
        save_format = output_filename.split('.')[-1].upper()
        if save_format not in ["JPEG", "PNG", "WEBP", "GIF"]: # Common formats Pillow supports
            save_format = "JPEG" # Fallback if extension is unknown
            # If we fall back to JPEG, ensure the filename extension is .jpg
            if not output_filename.lower().endswith(".jpg") and not output_filename.lower().endswith(".jpeg"):
                output_filename = os.path.splitext(output_filename)[0] + ".jpg"
                temp_output_path = os.path.join(temp_dir, output_filename) # Reconstruct path

        image.save(temp_output_path, format=save_format, optimize=True, quality=quality)
        
        # 7. Calculate and prepare the message
        new_size = os.path.getsize(temp_output_path) / 1024 # Size in KB
        message = f"Compression complete! Reduced Size: {new_size:.2f} KB. Ready for download."
        
        # 8. Set the output_filepath to the temporary file's path
        output_filepath = temp_output_path

    except Exception as e:
        message = f"An error occurred during processing: {e}"
        output_filepath = None
    finally:
        # IMPORTANT: Gradio itself handles the cleanup of the *returned* temporary file path.
        # However, for the temporary *directory* we created, we should clean it up
        # after Gradio has had a chance to process the file.
        # This is a bit tricky with asynchronous Gradio calls, but in practice,
        # Gradio often cleans up the directory where the file was.
        # For simplicity and to avoid race conditions with Gradio's internal cleanup,
        # we'll rely on Gradio for the cleanup of the file itself.
        # If temp_dir needs explicit cleanup, it's often done with a 'atexit' handler
        # or by Gradio's internal mechanisms for session-specific temp files.
        pass # Rely on Gradio's cleanup for the returned path.


    # 9. Return the results for Gradio outputs
    # For gr.File output, we return a filepath string (or None).
    # For gr.Textbox output, we return the message string.
    return output_filepath, message

# Define the Gradio Interface
iface = gr.Interface(
    fn=compress_image, # The function that Gradio will call
    inputs=[
        gr.Image(type="filepath", label="Upload an Image"), # Input expects a file path string
        gr.Textbox(label="Output Filename (e.g., compressed_image.jpg)", value="compressed_image.jpg"),
        gr.Slider(minimum=1, maximum=100, value=75, label="Image Quality (1-100)")
    ],
    outputs=[
        gr.File(label="Download Compressed Image"), # This is correct for returning a filepath
        gr.Textbox(label="Compression Info") # Text output for messages
    ],
    title="Image Compressor",
    description="Upload an image, choose an output filename and quality, and download the compressed version."
)

# Launch the Gradio app (only runs when you execute app.py directly)
if __name__ == "__main__":
    print("Successfully loaded your Gradio app. Starting local server...")
    iface.launch(debug=True)