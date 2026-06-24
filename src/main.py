from choose import step_choose
from compose import step_compose
from uploader import step_upload
from data import Data

if __name__ == "__main__":
    print("Loading data...")
    d = Data.load()
    print("Choosing files...")
    files = step_choose(d)

    print("Composing video...")
    path  = step_compose(d, files)

    print("Uploading video...")
    video = step_upload(d, path)

    print("Done!")
    print(f"Video uploaded to: {video}")
    

