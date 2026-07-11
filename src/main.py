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

    # action = input('What would you like to do? ["create", "delete", "rewrite", "print", "upload"]: ')
    action = "full"

    """ Full Workflow """
    if action == "full":
        print("Choosing files...")
        files = step_choose(d)

        print("Composing video...")
        path = step_compose(d, files)

        print("Uploading video...")
        video = step_upload(path)

        print("Done!")

    
    """ Create a video """
    if action == "create":
        choose = input("Choose specific files? [y/n]: ")
        if choose == "y":
            bg_path, meme_path, face_path, music_path = select_paths()
        else:
            bg_path = meme_path = face_path = music_path = None
            
        print("Choosing files...")
        files = step_choose(d, bg_path=bg_path, meme_path=meme_path, face_path=face_path, music_path=music_path)

        print("Composing video...")
        path  = step_compose(d, files)
    

    """ Delete a video """
    if action == "delete":
        id = int(input("What is the video id? "))
        d.del_comp(id)

    
    """ Rewrite a video """
    if action == "rewrite":
        id = int(input("What is the video id? "))
        bg_path, meme_path, face_path, music_path = select_paths()
        old_bg_path, old_meme_path, old_face_path, old_music_path, output_path = d.get_comp_files(id)

        if bg_path == None: bg_path = old_bg_path
        if meme_path == None: meme_path = old_meme_path
        if face_path == None: face_path = old_face_path
        if music_path == None: music_path = old_music_path

        files = (bg_path, meme_path, face_path, music_path, output_path, id)
        path = step_compose(d, files, rewrite=True)

        print("Rewriting composition data")
        d.rewrite_comp(id, bg_path=bg_path, meme_path=meme_path, face_path=face_path, music_path=music_path)
        d.clean_file_stats()

        print("Done!")

    """ Upload a video """
    if action == "upload":
        id = int(input("What is the video id? "))
        path = os.path.join(OUTPUTS_PATH, f"{id}.mp4")

        print("Uploading video...")
        video = step_upload(path)


    """ Print data """
    if action == "print":
        pprint.pprint(vars(d))
