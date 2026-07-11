from PIL import Image
from rembg import remove
from pillow_heif import register_heif_opener
from pydub import AudioSegment
from constants import *
from data import Data
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
        except Exception as e:
            print(f"Error converting {input_path} from webp to jpg: {e}") 

# Raw memes -> Ready memes
def convert_raw_memes(d, input_folder, output_folder):
    files = os.listdir(input_folder)

    output_map = {
        ".mp4": ".mp4",
        ".webp": ".jpg"
    }

    for file in files:
        root, ext = os.path.splitext(file)
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, f"{root}{output_map[ext]}")

        if os.path.isfile(output_path) or d.check_download("meme", input_path):
            os.remove(input_path)
            continue

        convert_meme(input_path, output_path, ext)
        os.remove(input_path)
        print(f"Saving {output_path}")
        

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
def convert_raw_faces(d, input_folder, output_folder):
    files = os.listdir(input_folder)
    
    for file in files:
        root, ext = os.path.splitext(file)
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, f"{root}.png")
        
        if os.path.isfile(output_path) or d.check_download("face", input_path): 
            os.remove(input_path)
            continue

        convert_face(input_path, output_path)
        os.remove(input_path)
        print(f"Saving {output_path}")



"""=============== MUSIC ==============="""

# Convert [m4a] to mp3
# def convert_music(folder):
#     files = os.listdir(folder)
    
#     for file in files:
#         root, ext = os.path.splitext(file)
#         input_path = os.path.join(folder, file)
#         output_path = os.path.join(folder, f"{root}.mp3")
#         if os.path.isfile(output_path): continue
#         print(f"Saving {output_path}")

#         if ext == "m4a":
#             audio = AudioSegment.from_file(input_path, format="m4a")
#             audio.export(output_path, format="mp3", bitrate="192k")
#             os.remove(input_path)


if __name__ == "__main__":
    d = Data.load()
    print("\nConverting memes...")
    convert_raw_memes(d, RAW_MEMES_PATH, READY_MEMES_PATH)

    print("\nConverting faces...")
    convert_raw_faces(d, RAW_FACES_PATH, READY_FACES_PATH)

    # print("\nConverting music...")
    # convert_music(MUSIC_PATH)


