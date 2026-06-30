from choose import step_choose, select_paths
from compose import step_compose
from uploader import step_upload
from constants import *
from data import Data
import pprint
import os


if __name__ == "__main__":

    print("Loading data...")
    d = Data.load()

    
    """ Create a video """
    create = input("Create new video? [y/n]: ")
    if create == "y":
        choose = input("Choose specific files? [y/n]: ")
        if choose == "y":
            bg_path, meme_path, face_path, music_path = select_paths()
            
        print("Choosing files...")
        files = step_choose(d, bg_path=bg_path, meme_path=meme_path, face_path=face_path, music_path=music_path)

        print("Composing video...")
        path  = step_compose(d, files)

        print("Uploading video...")
        video = step_upload(d, path)

        print("Done!")
        print(f"Video uploaded to: {video}")

    

    """ Delete a video """
    delete = input("Delete a composition? [y/n]: ")
    if delete == "y":
        id = int(input("What is the video id? "))
        d.del_comp(id)

    
    """ Rewrite a video """
    rewrite = input("Rewrite a composition? [y/n]: ")
    if rewrite == "y":
        id = int(input("What is the video id? "))
        bg_path, meme_path, face_path, music_path = select_paths()

        print("Choosing files...")
        files = step_choose(d, id=id, bg_path=bg_path, meme_path=meme_path, face_path=face_path, music_path=music_path)

        print("Composing video...")
        path  = step_compose(d, files)

        print("Uploading video...")
        video = step_upload(d, path)

        print("Rewriting composition data")
        d.rewrite_comp(id, bg_path=bg_path, meme_path=meme_path, face_path=face_path, music_path=music_path)

        print("Done!")
        print(f"Video uploaded to: {video}")


    """ Print data """
    print_data = input("Print current data? [y/n]: ")
    if print_data == "y":
        pprint.pprint(vars(d))
