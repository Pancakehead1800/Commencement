"""
Example of the Data structure:
{
    "count": 2,
    "opens": [0, 3, 16]
    "comps": 
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

        self.stats["bg_stats"]    = {}
        self.stats["meme_stats"]  = {}
        self.stats["face_stats"]  = {}
        self.stats["music_stats"] = {}

    # Get next id
    def get_next_id(self) -> int:
        res = 0
        if len(self.opens) == 0:
            print("Using count")
            res = self.count
        else:
            print("Using opens")
            res = self.opens[0]
            self.opens = self.opens[1:]
        return res
    
    
    # Check if we have already downloaded this file before
    def check_download(self, purpose, file) -> bool:
        if file in self.stats[purpose + "_stats"]:
            return True
        return False

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
        elif (id - self.stats[purpose]["last_used"] - 1) > time_between:
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
    def update_rewrite_file_stats(self, purpose, file, id) -> None:
        purpose_stats = f"{purpose}_stats"
        
        if file in self.stats[purpose_stats]:
            self.stats[purpose_stats][file]["count"] += 1
            self.stats[purpose_stats][file]["last_used"].add(id)
        else:
            self.stats[purpose_stats][file] = {}
            self.stats[purpose_stats][file]["count"] = 1
            self.stats[purpose_stats][file]["last_used"] = SortedList([id])
            
        old_file = self.comps[id][purpose]
        self.stats[purpose_stats][old_file]["count"] -= 1
        self.stats[purpose_stats][old_file]["last_used"].remove(id)
        return None
    
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
        self.count -= 1
        return None
    
    # Rewrite composition with different files
    def rewrite_comp(self, id, bg_path=None, meme_path=None, face_path=None, music_path=None) -> None:
        if bg_path != None:
            self.update_rewrite_file_stats("bg", bg_path, id)
            self.comps[id]["bg"] = bg_path
        if meme_path != None:
            self.update_rewrite_file_stats("meme", meme_path, id)
            self.comps[id]["meme"] = meme_path
        if face_path != None:
            self.update_rewrite_file_stats("face", face_path, id)
            self.comps[id]["face"] = face_path
        if music_path != None:
            self.update_rewrite_file_stats("music", music_path, id)
            self.comps[id]["music"] = music_path
        self.save()

    # Get current files for certain composition
    def get_comp_files(self, id):
        bg = self.comps[id]["bg"]
        meme = self.comps[id]["meme"]
        face = self.comps[id]["face"]
        music = self.comps[id]["music"]
        output = self.comps[id]["path"]
        return (bg, meme, face, music, output)

    # Clean all file stats based on compositions
    def clean_file_stats(self):
        count = 0

        self.stats = {"bg_stats": {}, "meme_stats": {}, "face_stats": {}, "music_stats": {}}

        for id, files in self.comps.items():
            count += 1

            bg = files["bg"]
            if bg not in self.stats["bg_stats"]:
                self.stats["bg_stats"][bg] = {"count": 0, "last_used": SortedList([])}
            self.stats["bg_stats"][bg]["count"] += 1
            self.stats["bg_stats"][bg]["last_used"].add(id)

            meme = files["meme"]
            if meme not in self.stats["meme_stats"]:
                self.stats["meme_stats"][meme] = {"count": 0, "last_used": SortedList([])}
            self.stats["meme_stats"][meme]["count"] += 1
            self.stats["meme_stats"][meme]["last_used"].add(id)

            face = files["face"]
            if face not in self.stats["face_stats"]:
                self.stats["face_stats"][face] = {"count": 0, "last_used": SortedList([])}
            self.stats["face_stats"][face]["count"] += 1
            self.stats["face_stats"][face]["last_used"].add(id)

            music = files["music"]
            if music not in self.stats["music_stats"]:
                self.stats["music_stats"][music] = {"count": 0, "last_used": SortedList([])}
            self.stats["music_stats"][music]["count"] += 1
            self.stats["music_stats"][music]["last_used"].add(id)
        
        self.count = count
        self.save()

    # get rid of double backslash // in the compositions
    # def clean_comps(self):
    #     for id, files in self.comps.items():
    #         for key, value in files.items():
    #             if isinstance(value, str):
    #                 self.comps[id][key] = value.replace("\\\\", "\\")
    #     self.save()
    
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
    d = Data.load()

    # Clear existing data
    wipe = input("Wipe all data? [y/n]: ")
    if wipe == "y":
        print("Wiping all data...")
        d = Data()
        d.save()

    # Clean all file stats
    clean = input("Clean all file stats? [y/n]: ")
    if clean == "y":
        print("Cleaning all file stats...")
        d.clean_comps()
        d.clean_file_stats()
        d.save()


    # Manually add composition data
    add = input("Add composition? [y/n]: ")
    while add == "y":
        id = int(input("Video id: "))
        bg = input("Full background path: ")
        meme = input("Full meme path: ")
        face = input("Full face path: ")
        music = input("Full music path: ")
        path = input("Full output path: ")
        duration = float(input("Duration: "))
        d.add_comp(bg, meme, face, music, path, duration, id)
        d.save()
        add = input("Add another composition? [y/n]: ")

    # Print existing data
    show = input("Print all data? [y/n]: ")
    if show == "y":
        pprint.pprint(vars(d))