from pathlib import Path
import shutil
import subprocess

from quickclone.config.common import USER_CACHE_FOLDER, CACHE_ITEMS

USER_CACHE_FOLDER_OLD = Path.home() / ".cache" / "quicktoml"
"""
Path to the incorrectly named cache folder: `~/.cache/quicktoml`
"""

def quickclone_cache_move() -> int:
    """
    Fix for v4.0 or below.
    
    Prompt user to move or copy cache from `~/.cache/quicktoml` to
    `~/.cache/quickclone`, then perform an operation based on the user's choice.
    See #Returns for what operations are available.
    The main logic of this function should only be activated if
    `~/.cache/quickclone` is not detected and `~/.cache/quicktoml` is non-empty.
    
    Returns
    -------
    status: int
        The status code indicates what operation was performed.
        0: Nothing had to be done, the cache folder is already at
            `~/.cache/quickclone` or if `~/.cache/quicktoml` was not detected.
        1: User didn't want to move `~/.cache/quicktoml` to
            `~/.cache/quickclone`.
        2: User moved `~/.cache/quicktoml` to `~/.cache/quickclone`.
        3: User copied `~/.cache/quicktoml` to `~/.cache/quickclone`.
    """
    # if ~/.cache/quickclone already exists
    if USER_CACHE_FOLDER.exists():
        return 0
    # detect useful ~/.cache/quicktoml
    if USER_CACHE_FOLDER_OLD.exists():
        if not USER_CACHE_FOLDER_OLD.is_dir():
            return 0
        # if ~/.cache/quicktoml empty
        try:
            next(USER_CACHE_FOLDER_OLD.iterdir())
        except StopIteration:
            return 0
    else:
        return
    print("⚠⚠⚠ WARNING ⚠⚠⚠")
    print(
        f"I made a mistake when writing the path of the cache folder, it was supposed to be at "
        f"'{USER_CACHE_FOLDER}' but instead I wrote '{USER_CACHE_FOLDER_OLD}'.",
        end="\n\n"
    )
    print(
        f"You can choose to either MOVE or COPY the contents of '{USER_CACHE_FOLDER_OLD}' "
        f"to '{USER_CACHE_FOLDER}'.",
        end="\n\n"
    )
    print(
        f"If you decide to move ALL of the contents of the cache "
        f"folder, any program that was using '{USER_CACHE_FOLDER_OLD}' cannot access their data at "
        f"that location. However, from what I know, no program other than QuickClone version 0.4.0 "
        f"and below uses this folder, so moving the cache folder should be safe.",
        end="\n\n"
    )
    print(
        f"If you choose to copy the cache from '{USER_CACHE_FOLDER_OLD}' to '{USER_CACHE_FOLDER}' "
        f"any program using '{USER_CACHE_FOLDER_OLD}' would have their data preserved, but this "
        f"would leave 2 copies of the same files inside each folder.",
        end="\n\n"
    )
    print("SELECT AN OPTION")
    print(f"1. MOVE contents of '{USER_CACHE_FOLDER_OLD}' to '{USER_CACHE_FOLDER}'.")
    print(f"2. COPY contents of '{USER_CACHE_FOLDER_OLD}' to '{USER_CACHE_FOLDER}'.")
    print(f"3. CANCEL")
    # prompt user whether to move directories
    answer = 0
    while True:
        answer = input("[1/2/3] ==> ")
        if answer in {"1", "2", "3"}:
            answer = int(answer)
            break
        else:
            print(f"Invalid answer: {answer}")
    ACTION = [_move_cache_folder, _copy_cache_folder, _exit_cache_move]
    return ACTION[answer-1]()


def _move_cache_folder() -> int:
    shutil.move(USER_CACHE_FOLDER_OLD, USER_CACHE_FOLDER)
    return 2

def _copy_cache_folder() -> int:
    subprocess.run(["mkdir", "-p", str(USER_CACHE_FOLDER)])
    for filename in CACHE_ITEMS:
        old = USER_CACHE_FOLDER_OLD / filename
        new = USER_CACHE_FOLDER / filename
        if old.exists():
            shutil.copy2(old, new)
    return 3
    
def _exit_cache_move() -> int:
    return 1
