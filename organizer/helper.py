import os
import config


def set_track_name(track_num: int) -> str:
    """Generate a track name based on the track number

    Args:
        track_num (int): The current track number

    Returns:
        str: The name of the track
    """
    if track_num < 10:
        track_name = f"track_0{track_num}{config.FILE_EXT}"
    else:
        track_name = f"track_{track_num}{config.FILE_EXT}"
    return track_name


def calc_merge_track_num(num_tracks: int, max_tracks: int) -> int:
    """Calculate the number of tracks to concatenate
    so that the final number of tracks generated is less than MAX_TRACKS

    Args:
        num_tracks (int): The number of tracks
        max_tracks (int): The maximum number of tracks possible

    Returns:
        int: The number of tracks to merge
    """
    merge_num = 1
    seeking_merge_num = True
    while seeking_merge_num:
        merge_num = merge_num + 1
        if(num_tracks / merge_num < max_tracks):
            seeking_merge_num = False
    return merge_num


def get_ordered_dirs(dir):
    """Order a list of directories by creation date

    Args:
        dir (str): Root path to source directory

    Returns:
        list: List of directories (str) ordered by creation date
    """
    return sorted(os.listdir(dir), key=lambda fn: os.path.getctime(os.path.join(dir, fn)))
