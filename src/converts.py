from PIL import Image

# .webp -> .jpg
def convert_webp_to_jpg(input_path, output_path):
    with Image.open(input_path) as image:
        image.save(output_path, "JPEG", quality=85, optimize=True)



