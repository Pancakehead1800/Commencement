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
    """Constants"""
    meme_w, meme_h = meme.w, meme.h
    ratio1 = meme_h / meme_w
    ratio2 = meme_w / meme_h

    """Resizing the meme"""
    # Approach 1: hit side bound
    new_w1 = VIDEO_WIDTH - 2 * SIDE_MEME_PADDING

    # Approach 2: hit lower bound
    new_h2 = VIDEO_HEIGHT - UPPDER_MEME_PADDING - LOWER_MEME_PADDING
    new_w2 = ratio2 * new_h2

    if new_w1 <= new_w2:
        meme_w = new_w1
        meme_h = ratio1 * meme_w
    elif new_w1 > new_w2:
        meme_w = new_w2
        meme_h = new_h2

    meme = meme.resized(width=meme_w, height=meme_h)

    """Positioning the meme"""
    cx = VIDEO_WIDTH / 2
    cy = UPPDER_MEME_PADDING + meme_h / 2

    x = cx - meme_w / 2
    y = cy - meme_h / 2

    meme = meme.with_position((x, y))
    return meme


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