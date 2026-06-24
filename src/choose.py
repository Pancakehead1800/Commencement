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
        last_used = d.stats[stats][file]["last_used"]
        if id - last_used - 1 >= TIME_BETWEEN_USE:
            res = file
            break

    if res == None:
        print(f"No good {purpose} file found!")
    
    return res


def get_next_id(d):
    return d.get_count() + 1
        

def get_all_random_files(d, id):
    bg_path    = get_random_file(d, "bg", id)
    meme_path  = get_random_file(d, "meme", id)
    face_path  = get_random_file(d, "face", id)
    music_path = get_random_file(d, "music", id)
    output_path = os.path.join(OUTPUTS_PATH, f"{id}.mp4")
    files = (bg_path, meme_path, face_path, music_path, output_path)
    return files
        

def step_choose(d):
    id = get_next_id(d)
    files = get_all_random_files(d, id)
    return files