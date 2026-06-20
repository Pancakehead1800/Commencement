from PIL import Image, ImageOps
from moviepy import ImageClip, VideoFileClip, CompositeVideoClip, AudioFileClip

WIDTH = 1080
HEIGHT = 1920

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
    bg = ImageClip(bg_path)
    meme = VideoFileClip(meme_path)
    face = ImageClip(face_path)
    music = AudioFileClip("music.mp3")

    # Preparing files
    duration = meme.duration
    bg = bg.resized(width=width, height=height).with_duration(duration).without_audio()
    meme = meme.resized(width=width * 0.8, height=height * 0.6).with_position(("center", "center"))
    face = face.resized(width=width * 0.75, height=height * 0.25).with_position(("center", height-face.h-50))
    audio = AudioFileClip(music_path).subclip(0, duration)

    # Compose files
    result = CompositeVideoClip([bg, meme, face], size=(width, height)).with_duration(duration).with_audio(audio)

    # Write result
    result.write_videofile(out_path, fps=30, codec="libx264", audio_codec="aac")
    return out_path

if __name__ == "__main__":
    image = make_composite(
        bg_path="./db_bgs/589516.jpg",
        meme_path="./db_memes/7772.mp4",
        face_path="./db_faces/red.jpg",
        out_path="./db_outputs/output.mp4",
        width=1080,
        height=1920,
    )
    # make_static_video(image, out_video="./db_outputs/clip.mp4", seconds=30)
    print("Done:", image, "and clip.mp4")