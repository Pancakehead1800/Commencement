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
    with open('data.json', 'r', encoding='utf-8') as file:
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
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)   

    # Create output path
    output_path = f"./db_outputs/{count}.mp4"
    
    return bg_path, meme_path, face_path, music_path, output_path

def position_bg(bg):
    W, H = 1080, 1920
    return bg.resized(width=W, height=H)

def position_meme(meme):
    # Side padding: 54px on each side -> width = 1080 - 2(54) = 972
    W, H = 1080, 1920 

    meme = meme.resized(width=972)

    x = 0.5 * W - meme.w / 2
    y = 0.35 * H - meme.h / 2

    return meme.with_position((x, y))

def position_face(face):
    # Face takes up 60% width of screen, with bottom edge on bottom
    W, H = 1080, 1920

    face = face.resized(width=int(0.6 * W))

    x = 0.5 * W - face.w / 2
    y = H - face.h

    return face.with_position((x, y))

def adjust_duration(meme):
    # if too short or too long, we want to slow down or speed up (up to maximum change, like 1.2 or 0.8)
    return meme.duration


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
    bg = position_bg(bg)
    meme = position_meme(meme)
    face = position_face(face)
    audio = audio.subclipped(0, duration)

    # Compose files
    result = CompositeVideoClip([bg, meme, face], size=(width, height))
    result = result.with_duration(duration)
    result = result.with_audio(audio)

    # Write result
    result.write_videofile(out_path, fps=30, codec="libx264", audio_codec="aac")
    return out_path

if __name__ == "__main__":
    bg_path, meme_path, face_path, music_path, output_path = get_random_files()
    bg_path     = "./db_bgs/sky1.mp4"
    meme_path   = "./db_memes/vtusv0dhbgq41.mp4"
    face_path   = "./db_faces/cat.png"
    music_path  = "./db_music/arab.mp3"
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