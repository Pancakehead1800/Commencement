import os
import random
from constants import *


def purpose_directories(purpose):
    purpose_map = {
        "bg":    (BGS_PATH,         "bg_stats"),
        "meme":  (READY_MEMES_PATH, "meme_stats"),
        "face":  (READY_FACES_PATH, "face_stats"),
        "music": (MUSIC_PATH,       "music_stats")    
    }
    return purpose_map[purpose]


def get_random_file(d, purpose, id):
    path, stats = purpose_directories(purpose)
    res = None

    i = 1
    while i < MAX_ITERATIONS:
        i += 1
        file = random.choice(os.listdir(path))

        last_used = 0
        if file in d.stats[stats]:
            last_used = d.stats[stats][file]["last_used"]
        else:
            last_used = 0

        if (last_used == 0) or (id - last_used - 1 >= TIME_BETWEEN_USE):
            res = file
            break

    if res == None:
        print(f"No good {purpose} file found!")
    
    return res


def get_next_id(d):
    return d.get_count() + 1
        

def get_all_random_files(
        d, id,
        bg_path=None,
        meme_path=None,
        face_path=None,
        music_path=None,
        output_path=None
    ):
    if bg_path == None:
        bg = get_random_file(d, "bg", id)
        bg_path    = os.path.join(BGS_PATH, bg)

    if meme_path == None:
        meme  = get_random_file(d, "meme", id)
        meme_path  = os.path.join(READY_MEMES_PATH, meme)

    if face_path == None:
        face  = get_random_file(d, "face", id)
        face_path  = os.path.join(READY_FACES_PATH, face)

    if music_path == None:
        music = get_random_file(d, "music", id)
        music_path = os.path.join(MUSIC_PATH, music)

    if output_path == None:
        output_path = os.path.join(OUTPUTS_PATH, f"{id}.mp4")

    files = (bg_path, meme_path, face_path, music_path, output_path, id)
    return files
        

def step_choose(d, bg_path=None, meme_path=None, face_path=None, music_path=None):
    id = get_next_id(d)
    files = get_all_random_files(d, id, bg_path=bg_path, meme_path=meme_path, face_path=face_path, music_path=music_path)
    return files