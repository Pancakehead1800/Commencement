from PIL import Image, ImageOps
from moviepy import ImageClip, VideoFileClip, CompositeVideoClip, AudioFileClip
import os
import random
import json

WIDTH = 1080
HEIGHT = 1920

def check_file_type(path):
    _, ext = os.path.splitext(path)
    ext = ext.lower()
    if ext == '.mp4':
        return 'mp4'
    elif ext == '.jpg':
        return 'jpg'
    else:
        return 'other'

def get_random_files():
    # Get random input files
    bg = random.choice(os.listdir("./db_bgs"))
    meme = random.choice(os.listdir("./db_memes"))
    face = random.choice(os.listdir("./db_faces"))
    music = random.choice(os.listdir("./db_music"))

    # Create input paths
    bg_path = f"./db_bgs/{bg}"
    meme_path = f"./db_memes/{meme}"
    face_path = f"./db_faces/{face}"
    music_path = f"./db_music/{music}"

    # Get next output number
    with open('./db_outputs/data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        count = data['count']
        count += 1
        data['count'] = count
        data[count] = {
            "bg": bg,
            "meme": meme,
            "face": face,
            "music": music
        }
    with open('./db_outputs/data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)   

    # Create output path
    output_path = f"./db_outputs/{count}.mp4"     

    return bg_path, meme_path, face_path, music_path, output_path

def make_composite(
    bg_path="./db_bgs/bg.jpg",
    meme_path="./db_memes/meme.jpg",
    face_path="./db_faces/face.jpg",
    music_path="./db_music/music.mp3",
    out_path="./db_outputs/output.mp4",
    width=1080,
    height=1920,
):
    # Load files
    bg_type = check_file_type(bg_path)
    if bg_type == 'mp4':
        bg = VideoFileClip(bg_path)
    else:
        bg = ImageClip(bg_path)
        
    face_type = check_file_type(face_path)
    if face_type == 'mp4':
        face = VideoFileClip(face_path)
    else:
        face = ImageClip(face_path)

    meme = VideoFileClip(meme_path)
    face = ImageClip(face_path)
    audio = AudioFileClip(music_path)

    # Preparing files
    duration = meme.duration
    bg = bg.resized(width=width, height=height).with_duration(duration).without_audio()
    meme = meme.resized(width=width * 0.5, height=height * 0.6).with_position(("center", 0.01 * height)) 
    face = face.resized(width=width * 0.75, height=height * 0.25).with_position(("center", height-face.h-50))
    audio = audio.subclipped(0, duration)

    # Compose files
    result = CompositeVideoClip([bg, meme, face], size=(width, height)).with_duration(duration).with_audio(audio)
    # result = CompositeVideoClip([bg, meme, face], size=(width, height)).with_duration(1.0).with_audio(audio)

    # Write result
    result.write_videofile(out_path, fps=30, codec="libx264", audio_codec="aac")
    return out_path

if __name__ == "__main__":
    bg_path, meme_path, face_path, music_path, output_path = get_random_files()
    image = make_composite(
        bg_path=bg_path,
        meme_path=meme_path,
        face_path=face_path,
        music_path=music_path,        
        out_path=output_path,
        width=1080,
        height=1920,
    )
    # make_static_video(image, out_video="./db_outputs/clip.mp4", seconds=30)
    print("Done:", image, "and clip.mp4")