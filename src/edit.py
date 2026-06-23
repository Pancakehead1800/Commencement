from PIL import Image, ImageOps
from moviepy import ImageClip, VideoFileClip, CompositeVideoClip, AudioFileClip
from moviepy.video.fx.Loop import Loop
from src.constants import *
import os
import random
import json


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
    bg    = random.choice(os.listdir(BGS_PATH))
    meme  = random.choice(os.listdir(READY_MEMES_PATH))
    face  = random.choice(os.listdir(FACES_PATH))
    music = random.choice(os.listdir(MUSIC_PATH))

    # Create input paths
    bg_path    = os.path.join(BGS_PATH, bg)
    meme_path  = os.path.join(READY_MEMES_PATH, meme)
    face_path  = os.path.join(FACES_PATH, face)
    music_path = os.path.join(MUSIC_PATH, music)

    # Get next output number
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        data["count"] = data.get("count", 0) + 1
        count = data["count"]
        data[count] = {
            "bg": bg,
            "meme": meme,
            "face": face,
            "music": music
        }

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)   

    # Create output path
    output_path = os.path.join(OUTPUTS_PATH, f"{count}.mp4")
    
    return bg_path, meme_path, face_path, music_path, output_path



def position_bg(bg):
    return bg.resized(width=VIDEO_WIDTH, height=VIDEO_HEIGHT)



def position_meme(meme, jitter_px=54):

    # Resize first so we know the final dimensions
    meme = meme.resized(width=972)
    w, h = meme.w, meme.h

    # Desired center point
    cx = 0.5 * VIDEO_WIDTH
    cy = 0.35 * VIDEO_HEIGHT

    # Convert center to top-left
    x = cx - w / 2
    y = cy - h / 2

    # Small random offset around that position  
    x += random.uniform(-jitter_px, jitter_px)
    y += random.uniform(-jitter_px, jitter_px)

    # Keep fully inside the window
    x = max(0, min(x, VIDEO_WIDTH - w))
    y = max(0, min(y, VIDEO_HEIGHT - h))

    return meme.with_position((x, y))



def position_face(face):
    # Face takes up 60% width of screen, with bottom edge on bottom
    W, H = 1080, 1920

    face = face.resized(width=int(0.6 * W))

    x = 0.5 * W - face.w / 2
    y = H - face.h

    return face.with_position((x, y))



def adjust_meme_duration(meme, duration):
    L_DURATION_BOUND = 5
    U_DURATION_BOUND = 50

    MAX_SPEEDUP = 1.2
    MAX_SLOWDOWN = 0.8

    if duration < L_DURATION_BOUND:
        speedup = min(MAX_SPEEDUP, L_DURATION_BOUND / duration)
        meme = meme.speedx(speedup)
    elif duration > U_DURATION_BOUND:
        slowdown = max(MAX_SLOWDOWN, U_DURATION_BOUND / duration)
        meme = meme.speedx(slowdown)

    return meme



def adjust_bg_duration(bg, duration):
    MAX_SPEEDUP = 10

    bg_duration = bg.duration

    if bg_duration < duration:
        speedup = min(MAX_SPEEDUP, duration / bg_duration)
        bg = bg.speedx(speedup)
    elif bg_duration > duration:
        bg = bg.with_effects([Loop(duration=duration)])

    return bg



def make_composite(
    bg_path=None,
    meme_path=None,
    face_path=None,
    music_path=None,
    output_path=None
) -> CompositeVideoClip:
    """Ensure file paths are given"""
    good = True
    if bg_path == None:
        print("Background not given")
        good = False
    if meme_path == None:
        print("Meme not given")
        good = False
    if face_path == None:
        print("Face not given")
        good = False
    if music_path == None:
        print("Music not given")
        good = False
    if output_path == None:
        print("Output not given")
        good = False

    if good == False:
        return None

    """Load files"""
    # Background file type
    bg_type = check_file_type(bg_path)
    if bg_type == 'mp4':
        bg = VideoFileClip(bg_path)
    else:
        bg = ImageClip(bg_path)
        
    # Face file type
    face_type = check_file_type(face_path)
    if face_type == 'mp4':
        face = VideoFileClip(face_path)
    else:
        face = ImageClip(face_path)

    # Meme file type
    meme_type = check_file_type(meme_path)
    if meme_type == "mp4":
        meme = VideoFileClip(meme_path)
    elif meme_type == "jpg":
        meme = ImageClip(meme_path)
    else:
        print(f"Bad meme file type: {meme_type}")

    face = ImageClip(face_path)
    audio = AudioFileClip(music_path)

    """Editing files"""
    duration = 0
    if meme_type == "mp4":
        duration = meme.duration
        meme = adjust_meme_duration(meme)
    elif meme_type == "jpg":
        duration = DEFAULT_MEME_DURATION

    bg    = adjust_bg_duration(bg, duration)
    bg    = position_bg(bg)
    meme  = position_meme(meme)
    face  = position_face(face)
    audio = audio.subclipped(0, duration)

    """Composing files"""
    result = CompositeVideoClip([bg, meme, face], size=(VIDEO_WIDTH, VIDEO_HEIGHT))
    result = result.with_duration(duration)
    result = result.with_audio(audio)

    """Writing result"""
    result.write_videofile(output_path, fps=FPS, codec="libx264", audio_codec="aac")
    return output_path



if __name__ == "__main__":
    bg_path, meme_path, face_path, music_path, output_path = get_random_files()
    print()
    print(f"Background: {bg_path}")
    print(f"Meme: {meme_path}")
    print(f"Face: {face_path}")
    print(f"Music: {music_path}")
    image = make_composite(
        bg_path=bg_path,
        meme_path=meme_path,
        face_path=face_path,
        music_path=music_path,        
        out_path=output_path,
    )
    # make_static_video(image, out_video="./db_outputs/clip.mp4", seconds=30)
    print("Done:", image, "and clip.mp4")