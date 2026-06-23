from moviepy import ImageClip, VideoFileClip, CompositeVideoClip, AudioFileClip
from moviepy.video.fx.Loop import Loop
from src.constants import *
import os
import random
import json


# Return file type
def check_file_type(path):
    _, ext = os.path.splitext(path)
    ext = ext.lower()
    if ext == '.mp4':
        return 'mp4'
    elif ext == '.jpg':
        return 'jpg'
    else:
        return 'other'


# Randomly choose files
def get_random_files():
    """Get random input files"""
    bg    = random.choice(os.listdir(BGS_PATH))
    meme  = random.choice(os.listdir(READY_MEMES_PATH))
    face  = random.choice(os.listdir(FACES_PATH))
    music = random.choice(os.listdir(MUSIC_PATH))

    """Create input paths"""
    bg_path    = os.path.join(BGS_PATH, bg)
    meme_path  = os.path.join(READY_MEMES_PATH, meme)
    face_path  = os.path.join(FACES_PATH, face)
    music_path = os.path.join(MUSIC_PATH, music)

    """Get next output number"""
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

    output_path = os.path.join(OUTPUTS_PATH, f"{count}.mp4")
    
    """Return"""
    return bg_path, meme_path, face_path, music_path, output_path


# Ensure background has proper dimensions
def position_bg(bg):
    return bg.resized(width=VIDEO_WIDTH, height=VIDEO_HEIGHT)


# Position the meme with slight randomness
def position_meme(meme):
    """Resize first so we know the final dimensions"""
    meme = meme.resized(width=VIDEO_WIDTH - 2 * JITTER_X)
    w, h = meme.w, meme.h

    """Center position"""
    cx = 0.5 * VIDEO_WIDTH
    cy = 0.35 * VIDEO_HEIGHT

    x = cx - w / 2
    y = cy - h / 2

    """Slight randomness"""
    x += random.uniform(-JITTER_X, JITTER_X)
    y += random.uniform(-JITTER_Y, JITTER_Y)

    x = max(0, min(x, VIDEO_WIDTH - w))
    y = max(0, min(y, VIDEO_HEIGHT - h))

    """Return"""
    return meme.with_position((x, y))


# Face should take 60% width and be flush to the bottom
def position_face(face):
    """Resizing"""
    face = face.resized(width=int(0.6 * VIDEO_WIDTH))

    """Positioning"""
    x = 0.5 * VIDEO_WIDTH - face.w / 2
    y = VIDEO_HEIGHT - face.h

    """Return"""
    return face.with_position((x, y))



def adjust_meme_duration(meme, duration):
    """Too short"""
    if duration < LOWER_DURATION_BOUND:
        speedup = min(MAX_MEME_SPEEDUP, LOWER_DURATION_BOUND / duration)
        meme = meme.speedx(speedup)

    """Too long"""
    if duration > UPPER_DURATION_BOUND:
        slowdown = max(MAX_MEME_SLOWDOWN, UPPER_DURATION_BOUND / duration)
        meme = meme.speedx(slowdown)

    """Return"""
    return meme



def adjust_bg_duration(bg, duration):
    bg_duration = bg.duration

    """Too short"""
    if bg_duration < duration:
        speedup = min(MAX_BG_SPEEDUP, duration / bg_duration)
        bg = bg.speedx(speedup)

    """Too long"""
    if bg_duration > duration:
        bg = bg.with_effects([Loop(duration=duration)])

    """Return"""
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