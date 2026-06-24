from compose import step_compose
from uploader import step_upload
from data import Data

if __name__ == "__main__":
    print("Loading data...")
    d = Data.load()
    print("Creating video...")
    output_path = step_compose(d)
    print("Uploading video...")
    step_upload(d)

