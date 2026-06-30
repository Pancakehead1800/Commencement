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

        last_used = d.stats[stats].get(file, {"last_used":0})["last_used"]

        if (last_used == 0):
            res = file
            break
            
        elif (purpose == "bg") and (d.check_file_usage("bg", file, id, TIME_BETWEEN_BGS):
            res = file
            break
            
        elif (purpose == "meme") and (d.check_file_usage("meme", file, id, TIME_BETWEEN_MEMES):
            res = file
            break
            
        elif (purpose == "face") and (d.check_file_usage("face", file, id, TIME_BETWEEN_FACES):
            res = file
            break
            
        elif (purpose == "music") and (d.check_file_usage("music", file, id, TIME_BETWEEN_MUSIC):
            res = file
            break

    if res == None:
        print(f"No good {purpose} file found!")
    
    return res


def get_next_id(d):
    return d.get_next_id()
        

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
        

def step_choose(d, id=None, bg_path=None, meme_path=None, face_path=None, music_path=None):
    id = get_next_id(d) if id == None else id
    files = get_all_random_files(d, id, bg_path=bg_path, meme_path=meme_path, face_path=face_path, music_path=music_path)
    return files