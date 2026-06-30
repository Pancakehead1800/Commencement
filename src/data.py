"""
Example of the Data structure:
{
    "count": 2,
    "opens": [0, 3, 16]
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
                "last_used": [1, 3]
            },
            "db_bgs/bg2.png":
            {
                "count": 1,
                "last_used": [2]
            }
        },
        "meme_stats":
        {
            "db_memes_ready/meme1.jpg": 
            {
                "count": 1,
                "last_used": [1]
            },
            "db_memes_ready/meme2.jpg": 
            {
                "count": 1,
                "last_used": [2, 3]
            }
        },
        "face_stats":
        {
            "db_faces_ready/face1.png":
            {
                "count": 2,
                "last_used": [2]
            }
        },
        "music_stats":
        {
            "db_music/music1.mp3": 
            {
                "count": 2,
                "last_used": [2]
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

import os
import pickle
from constants import *
import pprint
from sortedcontainers import SortedList

class Data:
    def __init__(self):
        self.count = 0
        self.opens = []
        self.comps = {}
        self.stats = {}
        self.files = {}

        self.stats["bg_stats"]    = {}
        self.stats["meme_stats"]  = {}
        self.stats["face_stats"]  = {}
        self.stats["music_stats"] = {}

        self.files["memes"] = set()
        self.files["faces"] = set()

    # Get next id
    def get_next_id(self) -> int:
        res = 0
        if len(self.opens) == 0:
            res = self.count
        else:
            res = self.opens[0]
            self.opens = self.opens[1:]
        return res
    
    
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
            self.stats[purpose][file]["last_used"].add(id)
        else:
            self.stats[purpose][file] = {"count": 1, "last_used": SortedList([id])}

        return None
        
    # Check if last usage of specified file was not long enough ago
    def check_file_usage(self, purpose, file, id, time_between) -> bool:
        purpose = f"{purpose}_stats"
        
        if file not in self.stats[purpose]:
            return True
        elif id < self.stats[purpose]["last_used"]:
            return True
        elif (id - self.stats[purpose]["last_used"] - 1) <= time_between:
            return True
        
        return False
    
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

    # Update file stats
    def update_file_stats(self, purpose, file, id) -> None:
        purpose = f"{purpose}_stats"
        if file in self.stats[purpose]:
            self.stats[purpose][file]["count"] += 1
            self.stats[purpose][file]["last_used"].add(id)
        else:
            self.stats[purpose][file] = {}
            self.stats[purpose][file]["count"] = 1
            self.stats[purpose][file]["last_used"] = SortedList([id])
    
    # Delete composition
    def del_comp(self, id) -> None:
        # Add id to self.opens
        n = len(self.opens)
        if n == 0: 
            self.opens.append(id)
        else:
            for i in range(n):
                if self.opens[i] > id:
                    self.opens = self.opens[:i] + [id] + self.opens[i:]
                    break
        # Remove data from self.comps
        self.comps[id] = {}
        return None
    
    # Rewrite composition with different files
    def rewrite_comp(self, id, bg_path=None, meme_path=None, face_path=None, music_path=None) -> None:
        if bg_path != None:
            self.comps[id][bg_path] = bg_path
            self.update_file_stats("bg", bg_path, id)
        if meme_path != None:
            self.comps[id][meme_path] = meme_path
            self.update_file_stats("meme", meme_path, id)
        if face_path != None:
            self.comps[id][face_path] = face_path
            self.update_file_stats("face", face_path, id)
        if music_path != None:
            self.comps[id][music_path] = music_path
            self.update_file_stats("music", music_path, id)
        self.save()
    
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
    print("Running data.py")

    # Clear existing data
    wipe = input("Wipe all data? [y/n]: ")
    if wipe.lower() in ["y", "yes"]:
        d = Data()
        d.save()

    # Print existing data
    d = Data.load()
    pprint.pprint(vars(d))