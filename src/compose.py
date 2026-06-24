from moviepy import ImageClip, VideoFileClip, CompositeVideoClip, AudioFileClip
from constants import *
from edits import *
import os
import random


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
def get_random_files(d):
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
    count = d.get_count()
    id = count + 1
    output_path = os.path.join(OUTPUTS_PATH, f"{id}.mp4")
    
    """Return"""
    return (bg_path, meme_path, face_path, music_path, output_path, id)


# Update data file with new upload
def update_data_files(d, files, duration, id):
    bg_path, meme_path, face_path, music_path, output_path, id = files
    d.add_composition(bg_path, meme_path, face_path, music_path, output_path, duration, id)
    d.use_file("bg", bg_path, id)
    d.use_file("meme", meme_path, id)
    d.use_file("face", face_path, id)
    d.use_file("music", music_path, id)
    d.save()
    

# Compose a video
def make_composite(files) -> CompositeVideoClip:
    """Unwrap"""
    bg_path, meme_path, face_path, music_path, output_path, id = files
    print(files)

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
        meme = ImageClip(meme_path).with_duration(DEFAULT_MEME_DURATION)
    else:
        print(f"Bad meme file type: {meme_type}")

    face = ImageClip(face_path)
    audio = AudioFileClip(music_path)

    """Editing files"""
    duration = 0
    if meme_type == "mp4":
        meme = adjust_meme_duration(meme)
        duration = meme.duration
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
    return output_path, duration, id


# Standard composition
def step_compose(d):
    files = get_random_files(d)
    output_path, duration, id = make_composite(files)
    update_data_files(d, files, duration, id)
    return output_path


# Testing
if __name__ == "__main__":
    from data import Data
    d = Data.load()
    step_compose(d)