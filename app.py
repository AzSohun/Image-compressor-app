# Upload image from Pc

from google.colab import files
from PIL import Image
import os

# Upload your image file
uploaded_file = files.upload()

# Store your uplaoded image into input file.
input_file = list(uploaded_file.keys())[0]

output_name = input("Enter output file name: ")

# If you don't put the file extention the it will
if "." not in output_name:
  output_name += ".jpg"

# Here you select you expected image quality
quality = int(input("Enter image quality (1 - 100): "))


# Now  it will open your image start the process
image = Image.open(input_file)


# Mode converter. It calls if needed
if image.mode in ("RGBA", "P"):
  image = image.convert("RBG")


# Set the image's max height and width.
max_width = 1280
max_height = 1280
image.thumbnail((max_width, max_height))

# Now to save the processed image
image.save(output_name, optimize=True, quality=quality)



# To Showing the original and reduced image size
original_size = os.path.getsize(input_file)
new_size = os.path.getsize(output_name)

print(f"Original Size: {original_size: .2f} KB")
print(f"Reduced Size: {new_size: .2f} KB")


# Download the compressed size image
files.download(output_name)