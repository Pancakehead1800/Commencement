from choose import step_choose
from compose import step_compose
from uploader import step_upload
from constants import *
from data import Data

if __name__ == "__main__":

    """ Very friendly UI for choosing specific files """
    """ Just enter the file name and don't worry about database folders """
    bg_path    = None
    meme_path  = None
    face_path  = None
    music_path = None

    if bg_path != None: bg_path = BGS_PATH + bg_path
    if meme_path != None: meme_path = READY_MEMES_PATH + meme_path
    if face_path != None: face_path = READY_FACES_PATH + face_path
    if music_path != None: music_path = MUSIC_PATH + music_path



    """ Main sequence """
    print("Loading data...")
    d = Data.load()

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


