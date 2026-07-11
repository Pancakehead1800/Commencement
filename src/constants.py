
# Video Dimensions
VIDEO_WIDTH  = 1080
VIDEO_HEIGHT = 1920

# Database Folder Paths
BGS_PATH         = "db/bgs"
RAW_MEMES_PATH   = "db/memes_raw"
READY_MEMES_PATH = "db/memes_ready"
RAW_FACES_PATH   = "db/faces_raw"
READY_FACES_PATH = "db/faces_ready"
MUSIC_PATH       = "db/music"
OUTPUTS_PATH     = "db/outputs"


# Data Storage
DATA_STORAGE_PATH = "states/data.pkl"
DATA_CLASS_PATH   = "src/data.py"


# File Choosing
MAX_ITERATIONS = 1000
TIME_BETWEEN_MEMES  = 15
TIME_BETWEEN_FACES  = 6
TIME_BETWEEN_BGS    = 1
TIME_BETWEEN_MUSICS = 1


# Video Specifications
DEFAULT_MEME_DURATION = 12
FPS = 30
PRIVACY_STATUS = "private"


# Background editing
MAX_BG_SPEEDUP = 20


# Meme Editing
UPPDER_MEME_PADDING  = 250
LOWER_MEME_PADDING   = 600
SIDE_MEME_PADDING    = 15
LOWER_DURATION_BOUND = 5
UPPER_DURATION_BOUND = 50
MAX_MEME_SPEEDUP     = 3.0
MAX_MEME_SLOWDOWN    = 0.3


# Face Editing
FACE_WIDTH = 0.7


# Secrets
SECRETS_FILE = "states/secrets.json"
TOKENS_FILE  = "states/tokens.json"