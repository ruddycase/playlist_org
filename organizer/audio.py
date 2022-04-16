#!/usr/bin/env python
import os
import config
from pathlib import Path


def _set_track_name(current_count):
    if current_count < 10:
        track_name = f"track_0{current_count}{config.FILE_EXT}"
    else:
        track_name = f"track_{current_count}{config.FILE_EXT}" 
    return track_name


def _calc_merge_track_num(num_tracks: int) -> int:
    """calculate the number of tracks to concatenate so that
    the final number of tracks generated is less than MAX_TRACKS"""
    merge_num = 1
    seeking_merge_num = True
    while seeking_merge_num:
        merge_num = merge_num + 1
        if(num_tracks/merge_num<config.MAX_TRACKS):
            seeking_merge_num = False
    return merge_num


def _get_ordered_dirs(dir):
    """order dirs by creation time"""
    return sorted(os.listdir(dir), key=lambda fn:os.path.getctime(os.path.join(dir, fn)))


def _generate_sequential_tracks(src_dir: str, dest_dir: str) -> None:
    for cd_dir in _get_ordered_dirs(src_dir):
        full_cd_dir = os.path.join(src_dir, cd_dir)
        last_track = 0
        if os.path.isdir(dest_dir):
            if os.path.isfile(config.CONTINUATION_FILE):
                with open(config.CONTINUATION_FILE, "r") as file:
                    last_track = int(file.read())
        else:
            Path(dest_dir).mkdir(parents=True, exist_ok=True)

        new_last_track = 0
        ordered_tracks = sorted(os.listdir(full_cd_dir), key=len)
        for idx, filename in enumerate(ordered_tracks, start=1):
            src_file = os.path.join(full_cd_dir, filename)
            track_num = last_track + idx
            new_last_track = track_num
            new_filename = _set_track_name(track_num)
            dest_file = os.path.join(dest_dir, new_filename)
            os.rename(src_file, dest_file)

        with open(config.CONTINUATION_FILE, "w") as file:
            file.write(str(new_last_track))


def _combine_tracks(dir: str, num_to_merge: int) -> None:
    audio_set_counter = 0
    counter = 0
    audio_set = None
    ordered_tracks = sorted(os.listdir(dir), key=len)
    for track in ordered_tracks:
        counter = counter + 1
        if audio_set:
            audio_set = audio_set + open(os.path.join(config.DEST_DIR, track), "rb").read()
            os.remove(os.path.join(config.DEST_DIR, track))
        else:
            audio_set = open(os.path.join(config.DEST_DIR, track), "rb").read()
            os.remove(os.path.join(config.DEST_DIR, track))
            continue
        if counter % num_to_merge == 0:
            audio_set_counter = audio_set_counter + 1
            set_name = _set_track_name(audio_set_counter)
            with open(os.path.join(config.DEST_DIR, set_name), "wb") as file:
                file.write(audio_set)
            audio_set = None

    if audio_set:
        audio_set_counter = audio_set_counter + 1
        set_name = _set_track_name(audio_set_counter)
        with open(os.path.join(config.DEST_DIR, set_name), "wb") as file:
            file.write(audio_set)
        audio_set = None


def main():
    print("Generating tracks...")
    _generate_sequential_tracks(config.SRC_DIR, config.DEST_DIR)

    with open(config.CONTINUATION_FILE, "r") as file:
        last_track = int(file.read())
    if os.path.exists(config.CONTINUATION_FILE):
        os.remove(config.CONTINUATION_FILE)

    if last_track > config.MAX_TRACKS:
        print("Combining tracks...")
        _combine_tracks(config.DEST_DIR, _calc_merge_track_num(last_track))

    print(f"Successfully created tracks at {config.DEST_DIR}")
    print(f"Please remove {config.SRC_DIR}")


if __name__ == "__main__":
    main()