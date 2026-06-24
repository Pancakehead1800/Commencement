from constants import *
import random
from moviepy import ImageClip, VideoFileClip, CompositeVideoClip, AudioFileClip
from moviepy.video.fx.Loop import Loop
from moviepy.video.fx import MultiplySpeed


# Ensure background has proper dimensions
def position_bg(bg):
    return bg.resized(width=VIDEO_WIDTH, height=VIDEO_HEIGHT)


# Position the meme with slight randomness
def position_meme(meme: ImageClip | VideoFileClip) -> ImageClip | VideoFileClip:
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
def position_face(face: ImageClip) -> ImageClip:
    """Resizing"""
    face = face.resized(width=int(FACE_WIDTH * VIDEO_WIDTH))

    """Positioning"""
    x = 0.5 * VIDEO_WIDTH - face.w / 2
    y = VIDEO_HEIGHT - face.h

    """Return"""
    return face.with_position((x, y))


def adjust_meme_duration(meme: VideoFileClip) -> VideoFileClip:
    duration = meme.duration
    """Too short"""
    if duration < LOWER_DURATION_BOUND:
        slowdown = max(MAX_MEME_SLOWDOWN, duration / LOWER_DURATION_BOUND)
        meme = meme.with_effects([MultiplySpeed(slowdown)])

    """Too long"""
    if duration > UPPER_DURATION_BOUND:
        speedup = min(MAX_MEME_SPEEDUP, UPPER_DURATION_BOUND / duration)
        meme = meme.with_effects([MultiplySpeed(speedup)])

    """Return"""
    return meme



def adjust_bg_duration(bg: VideoFileClip, duration: float) -> VideoFileClip:
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