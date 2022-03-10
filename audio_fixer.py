#!/usr/bin/env python
import os
from pathlib import Path

SRC_DIR = ""
DEST_DIR = ""
CONTINUATION_FILE = os.path.join(DEST_DIR, "last_track.txt")
MAX_TRACKS = 128
FILE_EXT = '.mp3'

def set_track_name(current_count):
    if current_count < 10:
        track_name = f"track_0{current_count}{FILE_EXT}"
    else:
        track_name = f"track_{current_count}{FILE_EXT}" 
    return track_name


def calc_merge_track_num(num_tracks: int) -> int:
    """calculate the number of tracks to concatenate so that
    the final number of tracks generated is less than 128"""
    merge_num = 1
    seeking_merge_num = True
    while seeking_merge_num:
        merge_num = merge_num + 1
        if(num_tracks/merge_num<MAX_TRACKS):
            seeking_merge_num = False
    return merge_num


def get_ordered_dirs(dir):
    """order dirs by creation time"""
    return sorted(os.listdir(dir), key=lambda fn:os.path.getctime(os.path.join(dir, fn)))


def main():
    for cd_dir in get_ordered_dirs(SRC_DIR):
        full_cd_dir = os.path.join(SRC_DIR, cd_dir)
        last_track = 0
        if os.path.isdir(DEST_DIR):
            if os.path.isfile(CONTINUATION_FILE):
                with open(CONTINUATION_FILE, "r") as file:
                    last_track = int(file.read())
        else:
            Path(DEST_DIR).mkdir(parents=True, exist_ok=True)

        new_last_track = 0
        ordered_tracks = sorted(os.listdir(full_cd_dir), key=len)
        for idx, filename in enumerate(ordered_tracks, start=1):
            src_file = os.path.join(full_cd_dir, filename)
            track_num = last_track + idx
            new_last_track = track_num
            new_filename = set_track_name(track_num)
            dest_file = os.path.join(DEST_DIR, new_filename)
            os.rename(src_file, dest_file)

        new_last_track = str(new_last_track)
        with open(CONTINUATION_FILE, "w") as file:
            file.write(new_last_track)

    if os.path.exists(CONTINUATION_FILE):
        os.remove(CONTINUATION_FILE)
    audio_set_counter = 0
    counter = 0
    audio_set = None
    ordered_tracks = sorted(os.listdir(DEST_DIR), key=len)
    num_tracks_to_merge = calc_merge_track_num(len(ordered_tracks))
    for track in ordered_tracks:
        counter = counter + 1
        if audio_set:
            audio_set = audio_set + open(os.path.join(DEST_DIR, track), "rb").read()
            os.remove(os.path.join(DEST_DIR, track))
        else:
            audio_set = open(os.path.join(DEST_DIR, track), "rb").read()
            os.remove(os.path.join(DEST_DIR, track))
            continue
        if counter % num_tracks_to_merge == 0:
            audio_set_counter = audio_set_counter + 1
            set_name = set_track_name(audio_set_counter)
            with open(os.path.join(DEST_DIR, set_name), "wb") as file:
                file.write(audio_set)
            audio_set = None

    if audio_set:
        audio_set_counter = audio_set_counter + 1
        set_name = set_track_name(audio_set_counter)
        with open(os.path.join(DEST_DIR, set_name), "wb") as file:
            file.write(audio_set)
        audio_set = None
    print(f"Successfully created tracks at {DEST_DIR}")
    print(f"Please remove {SRC_DIR}")

if __name__ == "__main__":
    main()