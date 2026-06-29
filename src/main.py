from choose import step_choose
from compose import step_compose
from uploader import step_upload
from constants import *
from data import Data
import os

if __name__ == "__main__":

    print("Loading data...")
    d = Data.load()

    """ Very friendly UI for choosing specific files """
    bg_path    = None
    meme_path  = None
    face_path  = None
    music_path = "end_of_beginning_sad.mp3"

    if bg_path != None: bg_path = os.path.join(BGS_PATH, bg_path)
    if meme_path != None: meme_path = os.path.join(READY_MEMES_PATH, meme_path)
    if face_path != None: face_path = os.path.join(READY_FACES_PATH, face_path)
    if music_path != None: music_path = os.path.join(MUSIC_PATH, music_path)

    
    """ Create a video """
    create = input("Create new video? [y/n]: ")
    if create == "y":
        print("Choosing files...")
        files = step_choose(d, bg_path=bg_path, meme_path=meme_path, face_path=face_path, music_path=music_path)

        print("Composing video...")
        path  = step_compose(d, files)

        print("Uploading video...")
        video = step_upload(d, path)

        print("Done!")
        print(f"Video uploaded to: {video}")

    

    """ Delete a video """
    delete = input("Delete a composition? [y/n]")
    if delete == "y":
        id = int(input("What is the video id? "))
        d.del_comp(id)

    
    """ Rewrite a video """
    rewrite = input("Rewrite a composition? [y/n]")
    if rewrite == "y":
        id = int(input("What is the video id? "))
        d.rewrite_comp(id, bg_path=bg_path, meme_path=meme_path, face_path=face_path, music_path=music_path)

        print("Choosing files...")
        files = step_choose(d, bg_path=bg_path, meme_path=meme_path, face_path=face_path, music_path=music_path)

        print("Composing video...")
        path  = step_compose(d, files)

        print("Uploading video...")
        video = step_upload(d, path)

        print("Done!")
        print(f"Video uploaded to: {video}")



    """ Because the uploader isn't working yet, just log the uploads here"""
    uploaded_files = [3, 2, 0]


