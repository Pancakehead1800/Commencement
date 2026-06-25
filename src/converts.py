from PIL import Image
from rembg import remove
from pillow_heif import register_heif_opener
from constants import *
import os


"""=============== MEMES ==============="""

# Raw meme -> Ready meme
def convert_meme(input_path, output_path, ext):
    """.mp4 memes are directly copied"""
    if ext == ".mp4":
        with open(input_path, "rb") as src:
            with open(output_path, "wb") as dst:
                dst.write(src.read())

    """.webp memes are converted to .jpg"""
    if ext == ".webp":
        try:
            with Image.open(input_path) as image:
                image.save(output_path, "JPEG", quality=85, optimize=True)
            os.remove(input_path)
        except Exception as e:
            print(f"Error converting {input_path} from webp to jpg: {e}") 

# Raw memes -> Ready memes
def convert_raw_memes(input_folder, output_folder):
    files = os.listdir(input_folder)

    output_map = {
        ".mp4": ".mp4",
        ".webp": ".jpg"
    }

    for file in files:
        root, ext = os.path.splitext(file)
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, f"{root}{output_map[ext]}")
        os.remove(input_path)
        if os.path.isfile(output_path): continue
        convert_meme(input_path, output_path)
        

"""=============== FACES ==============="""

    
# Remove bg for faces
def convert_face(input_path, output_path):
    register_heif_opener()
    try:
        with Image.open(input_path) as image:
            output_image = remove(image)
            output_image.save(output_path)
    except Exception as e:
        print(f"Error converting {input_path} from jpg to png without background: {e}")

# Remove all bg
def convert_raw_faces(input_folder, output_folder):
    files = os.listdir(input_folder)
    
    for file in files:
        root, ext = os.path.splitext(file)
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, f"{root}.png")
        os.remove(input_path)
        if os.path.isfile(output_path): continue
        convert_face(input_path, output_path)


if __name__ == "__main__":
    convert_raw_memes(RAW_MEMES_PATH, READY_MEMES_PATH)
    convert_raw_faces(RAW_FACES_PATH, READY_FACES_PATH)


