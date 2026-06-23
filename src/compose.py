from moviepy import ImageClip, VideoFileClip, CompositeVideoClip, AudioFileClip
from constants import *
from edits import *
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
    

# Ensure json data file is setup
def clean_data_file():
    with open("data.json", "r", encoding="utf-8") as file: 
        data = json.load(file)

        # Upload counter
        if "count" not in data:
            data["count"] = 0
        
        # Complete compositions
        if "compositions" not in data:
            data["compositions"] = {}

        # Files usage statistics
        if "statistics" not in data:
            data["statistics"] = {}



# Randomly choose files
def get_random_files():
    """Get random input files"""
    bg    = random.choice(os.listdir(BGS_PATH))
    meme  = random.choice(os.listdir(READY_MEMES_PATH))
    face  = random.choice(os.listdir(READY_FACES_PATH))
    music = random.choice(os.listdir(MUSIC_PATH))

    """Create input paths"""
    bg_path    = os.path.join(BGS_PATH, bg)
    meme_path  = os.path.join(READY_MEMES_PATH, meme)
    face_path  = os.path.join(READY_FACES_PATH, face)
    music_path = os.path.join(MUSIC_PATH, music)

    """Get next output number"""
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        count = data.get("count", 0) + 1
        
    output_path = os.path.join(OUTPUTS_PATH, f"{count}.mp4")
    
    """Return"""
    return bg_path, meme_path, face_path, music_path, output_path


# Update data file with new upload
# NOTE: "count" represents the new upload number
def update_data_file(bg_path, meme_path, face_path, music_path, count):
    with open("data.json", "w", encoding="utf-8") as file:
        data = json.load(file)

        # Update count
        data["count"] = count

        # Add new composition data
        data["compositions"][count] = {
            "bg":    bg_path,
            "meme":  meme_path,
            "face":  face_path,
            "music": music_path
        }

        # Update file statistics
        data["statistics"][bg_path]    = data["statistics"].get(bg_path, 0)    + 1
        data["statistics"][meme_path]  = data["statistics"].get(meme_path, 0)  + 1
        data["statistics"][face_path]  = data["statistics"].get(face_path, 0)  + 1
        data["statistics"][music_path] = data["statistics"].get(music_path, 0) + 1

        # Write new data
        json.dump(data, file, indent=4, ensure_ascii=False) 



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
    
    print("Done:", image, "and clip.mp4")