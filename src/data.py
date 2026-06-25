"""
Example of the Data structure:
{
    "count": 2,
    "compositions": 
    {
        "1": 
        {
            "bg": "db_bgs/bg1.png",
            "meme": "db_memes_ready/meme1.jpg",
            "face": "db_faces_ready/face1.png",
            "music": "db_music/music1.mp3",
            "path": "db_outputs/1.mp4",
            "duration": 10
        },
        "2": 
        {
            "bg": "db_bgs/bg2.png",
            "meme": "db_memes_ready/meme2.jpg",
            "face": "db_faces_ready/face1.png",
            "music": "db_music/music1.mp3",
            "path": "db_outputs/2.mp4",
            "duration": 12
        }
    },
    "stats": 
    {
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
            "db_memes_ready/meme1.jpg": 
            {
                "count": 1,
                "last_used": 1
            },
            "db_memes_ready/meme2.jpg": 
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
    },
    "files":
    {
        "memes": set{meme1.webp, meme2.webp},
        "faces": set{face1.jpg, face2.heic}
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

import os
import pickle
from constants import *

class Data:
    def __init__(self):
        self.count = 0
        self.comps = {}
        self.stats = {}
        self.files = {}

        self.stats["bg_stats"]    = {}
        self.stats["meme_stats"]  = {}
        self.stats["face_stats"]  = {}
        self.stats["music_stats"] = {}

        self.files["memes"] = set()
        self.files["faces"] = set()

    # Get composition count
    def get_count(self) -> int:
        return self.count
    
    # Check if we have already downloaded this file before
    def check_download(self, purpose, file) -> bool:
        purpose = purpose + "s"
        if file in self.files[purpose]:
            return False
        return True

    # Update the statistics of the file
    def use_file(self, purpose, file, id) -> None:
        purpose = f"{purpose}_stats"

        if file in self.stats[purpose]:
            self.stats[purpose][file]["count"] += 1
            self.stats[purpose][file]["last_used"] = id
        else:
            self.stats[purpose][file] = {"count": 1, "last_used": id}

        return None
    
    # Add new composition
    def add_comp(self, bg, meme, face, music, path, duration, id) -> None:
        self.count += 1
        self.comps[id] = {
            "bg":       bg,
            "meme":     meme,
            "face":     face,
            "music":    music,
            "path":     path,
            "duration": duration
        }
        return None
    
    # Save data to data.pkl
    def save(self):
        with open(DATA_STORAGE_PATH, "wb") as file:
            pickle.dump(self, file)

    # Load data from data.pkl
    @classmethod
    def load(cls):
        with open(DATA_STORAGE_PATH, "rb") as file:
            return pickle.load(file)


if __name__ == "__main__":
    # Clear existing data
    wipe = input("Wipe all data? [y/n]: ")
    if wipe.lower() in ["y", "yes"]:
        d = Data()
        d.save()