import os

# directory of source audio tracks
SRC_DIR = "C:\\Some\\path\\to\\audio\\tracks"

# directory where transformed audio tracks should be placed
DEST_DIR = "C:\\Some\\destination\\path"

# file to maintain track number
CONTINUATION_FILE = os.path.join(DEST_DIR, "last_track.txt")

# maximum number of tracks to generate
MAX_TRACKS = 128

# default source AND destination track file extension
FILE_EXT = '.mp3'