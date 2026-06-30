import os
import random
from constants import *


def select_paths():
    print("\nIf no specific file chosen, leave input blank")
    bg_path = input("Enter background path: ")
    meme_path = input("Enter meme path: ")
    face_path = input("Enter face path: ")
    music_path = input("Enter music path: ")

    if bg_path == "": bg_path = None
    if meme_path == "": meme_path = None
    if face_path == "": face_path = None
    if music_path == "": music_path = None

    # bg_path = os.path.join(BGS_PATH, bg_path) if bg_path != "" else None
    # meme_path = os.path.join(READY_MEMES_PATH, meme_path) if meme_path != "" else None
    # face_path = os.path.join(READY_FACES_PATH, face_path) if face_path != "" else None
    # music_path = os.path.join(MUSIC_PATH, music_path) if music_path != "" else None

    return bg_path, meme_path, face_path, music_path


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
            
        elif (purpose == "bg") and (d.check_file_usage("bg", file, id, TIME_BETWEEN_BGS)):
            res = file
            break
            
        elif (purpose == "meme") and (d.check_file_usage("meme", file, id, TIME_BETWEEN_MEMES)):
            res = file
            break
            
        elif (purpose == "face") and (d.check_file_usage("face", file, id, TIME_BETWEEN_FACES)):
            res = file
            break
            
        elif (purpose == "music") and (d.check_file_usage("music", file, id, TIME_BETWEEN_MUSICS)):
            res = file
            break

    if res == None:
        print(f"No good {purpose} file found!")
    
    return res


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
    id = d.get_next_id() if id == None else id
    files = get_all_random_files(d, id, bg_path=bg_path, meme_path=meme_path, face_path=face_path, music_path=music_path)
    return files