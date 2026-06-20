from rembg import remove
from PIL import Image

# Load image
input_path = './db_faces/e.png'
output_path = 'output.png'

# Remove background
input_image = Image.open(input_path)
output_image = remove(input_image)

# Save result with transparent background
output_image.save(output_path)   