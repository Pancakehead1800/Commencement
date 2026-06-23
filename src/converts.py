from PIL import Image
import os

# .webp -> .jpg
def convert_webp_to_jpg(input_path, output_path):
    try:
        with Image.open(input_path) as image:
            image.save(output_path, "JPEG", quality=85, optimize=True)
    except Exception as e:
        print(f"Error converting {input_path} from webp to jpg: {e}") 


# .webp -> jpg FOR ALL .webp IN db_memes_raw
def convert_all_webp_to_jpg(input_folder, output_folder):
    files = os.listdir(input_folder)

    for file in files:
        root, ext = os.path.splitext(file)
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, f"{root}.jpg")
        if os.path.isfile(output_path):
            continue
        convert_webp_to_jpg(input_path, output_path)


convert_all_webp_to_jpg("db_memes_raw", "db_memes_ready")
