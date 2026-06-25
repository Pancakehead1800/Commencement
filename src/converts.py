from PIL import Image
from rembg import remove
from pillow_heif import register_heif_opener
from constants import *
import os

# .webp -> .jpg
# Used for: Memes
def convert_webp_to_jpg(input_path, output_path):
    try:
        with Image.open(input_path) as image:
            image.save(output_path, "JPEG", quality=85, optimize=True)
        os.remove(input_path)
    except Exception as e:
        print(f"Error converting {input_path} from webp to jpg: {e}") 


# .webp -> jpg FOR ALL .webp IN db_memes_raw
# Used for: Memes
def convert_raw_memes(input_folder, output_folder):
    files = os.listdir(input_folder)

    for file in files:
        root, ext = os.path.splitext(file)
        input_path = os.path.join(input_folder, file)
        if ext == ".mp4":
            output_path = os.path.join(output_folder, f"{root}.mp4")
            if os.path.isfile(output_path):
                continue
            with open(input_path, "rb") as src:
                with open(output_path, "wb") as dst:
                    dst.write(src.read())
            os.remove(input_path)

        else:
            output_path = os.path.join(output_folder, f"{root}.jpg")
            if os.path.isfile(output_path):
                continue
            convert_webp_to_jpg(input_path, output_path)
        
    
# Remove bg
# Used for: Faces
def convert_to_clear_png(input_path, output_path):
    register_heif_opener()
    try:
        with Image.open(input_path) as image:
            output_image = remove(image)
            output_image.save(output_path)
    except Exception as e:
        print(f"Error converting {input_path} from jpg to png without background: {e}")

# Remove all bg
# Used for: Faces
def convert_all_to_clear_png(input_folder, output_folder):
    files = os.listdir(input_folder)
    
    for file in files:
        root, ext = os.path.splitext(file)
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, f"{root}.png")
        if os.path.isfile(output_path):
            continue
        convert_to_clear_png(input_path, output_path)


if __name__ == "__main__":
    convert_raw_memes(RAW_MEMES_PATH, READY_MEMES_PATH)
    convert_all_to_clear_png(RAW_FACES_PATH, READY_FACES_PATH)


