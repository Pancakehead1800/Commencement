"""
Example of the Data structure:
{
    "count": 2,
    "compositions": 
    {
        "1": 
        {
            "bg": "db_bgs/bg1.png",
            "meme": "db_memes_ready/meme1.png",
            "face": "db_faces_ready/face1.png",
            "music": "db_music/music1.mp3",
            "path": "db_outputs/1.mp4",
            "duration": 10
        },
        "2": 
        {
            "bg": "db_bgs/bg2.png",
            "meme": "db_memes_ready/meme2.png",
            "face": "db_faces_ready/face1.png",
            "music": "db_music/music1.mp3",
            "path": "db_outputs/2.mp4",
            "duration": 12
        }
    },
    "bg_stats":
    {
        "db_bgs/bg1.png": 
        {
            "count": 1,
            "last_used": 1
        },
        "db_bgs/bg2.png":
        {
            "count": 1,
            "last_used": 2
        }
    },
    "meme_stats":
    {
        "db_memes_ready/meme1.png": 
        {
            "count": 1,
            "last_used": 1
        },
        "db_memes_ready/meme2.png": 
        {
            "count": 1,
            "last_used": 2
        }
    },
    "face_stats":
    {
        "db_faces_ready/face1.png":
        {
            "count": 2,
            "last_used": 2
        }
    },
    "music_stats":
    {
        "db_music/music1.mp3": 
        {
            "count": 2,
            "last_used": 2
        }
    }
}
"""


"""
Functions to include:

def get_count() ->
    return data["count"]

def use_file(purpose, file, id) -> 
    data[f"{purpose}_stats"][file]["count"] += 1
    data[f"{purpose}_stats"][file]["last_used"] = id
    return None

def add_composition(bg, meme, face, music, path, duration, id) ->
    data["count"] += 1
    data["compositions"][id] = {"bg": bg, "meme": meme, "face": face, "music": music, "path": path, "duration": duration}
    return None

def write_data() -> 
    pickle.write_the_data

def read_data() ->
    pickle.get_the_data
"""

import pickle
from constants import *

class Data:
    def __init__(self):
        self.count        = 0
        self.compositions = {}
        self.bg_stats     = {}
        self.meme_stats   = {}
        self.face_stats   = {}
        self.music_stats  = {}

    def get_count(self) -> int:
        return self.count
    
    def use_file(self, purpose, file, id) -> None:
        purpose = f"{purpose}_stats"

        if file not in self.purpose:
            self.purpose[file] = {"count": 0, "last_used": 0}
        
        self.purpose[file]["count"] += 1
        self.purpose[file]["last_used"] = id
        return None
    
    def add_composition(self, bg, meme, face, music, path, duration, id) -> None:
        self.count += 1
        self.compositions[id] = {
            "bg":       bg,
            "meme":     meme,
            "face":     face,
            "music":    music,
            "path":     path,
            "duration": duration
        }
        return None
    
    def save_data(self):
        with open(DATA_STORAGE_PATH, "wb") as file:
            pickle.dump(self, file)

    @classmethod
    def load_data(cls):
        with open(DATA_STORAGE_PATH, "rb") as file:
            return pickle.load(file)
