from __future__ import annotations
from pathlib import Path
import typing as t
import subprocess

import toml

from .common import USER_CACHE_FOLDER, USER_HISTORY_CACHE_FILE

AVAILABLE_CACHES: t.Set[str] = {"history"}
"""
The available cache data categories.
"""

_HISTORY_CACHE: t.Dict[str, t.Any] = dict()

def _create_file_if_not_exist(path: Path) -> None:
    if not path.exists():
        open(path, "x")

def load_caches(cache_names: t.Iterable[str]) -> int:
    """
    Load the data belonging to certain cache data categories.
    
    Parameters
    ----------
    cache_name: Iterable[str]
        List of cache categories to load up. Only the values that exist in
        `quickclone.config.cache.AVAILABLE_CACHES` are allowed.
    
    Raises
    ------
    ValueError
        If an invalid cache category name was given.
    
    Returns
    -------
    int
        The number of cache categories loaded.
    """
    subprocess.run(["mkdir", "-p", str(USER_CACHE_FOLDER)])
    count = 0
    for cache_name in cache_names:
        if cache_name == "history":
            _create_file_if_not_exist(USER_HISTORY_CACHE_FILE)
            global _HISTORY_CACHE
            _HISTORY_CACHE = toml.load(USER_HISTORY_CACHE_FILE)
        else:
            raise ValueError(f"Invalid cache name given: {cache_name}")
        count += 1
    return count

def _check_is_dict(obj: object) -> bool:
    return isinstance(obj, dict)

def _assert_is_dict(obj: object) -> None:
    assert _check_is_dict(obj), "Expected cache object to be an instance of a dictionary."

def _dump_cache(path: Path, cache: t.Dict[str, t.Any]) -> None:
    with open(path, "w") as f:
        toml.dump(cache, f)

def dump_caches(cache_names: t.Iterable[str]) -> int:
    """
    Dump the data belonging to certain cache data categories to their corresponding file.
    
    Parameters
    ----------
    cache_name: Iterable[str]
        List of cache categories to dump. Only the values that exist in
        `quickclone.config.cache.AVAILABLE_CACHES` are allowed.
    
    Raises
    ------
    ValueError
        If an invalid cache category name was given.
    
    Returns
    -------
    int
        The number of cache categories dumped.
    """
    subprocess.run(["mkdir", "-p", str(USER_CACHE_FOLDER)])
    count = 0
    for cache_name in cache_names:
        if cache_name == "history":
            _assert_is_dict(_HISTORY_CACHE)
            _dump_cache(USER_HISTORY_CACHE_FILE, _HISTORY_CACHE)
        else:
            raise ValueError(f"Invalid cache name given: {cache_name}")
    return count

def get_cache_value(desired: str) -> t.Optional[t.Any]:
    """
    Get cache value of desired key.
    """
    if desired == "last_clone":
        return _HISTORY_CACHE.get("last_clone")
    else:
        raise ValueError(f"Invalid desired={desired}")

def set_cache_value(desired: str, value: t.Optional[t.Any] = None) -> None:
    """
    Set cache value of desired key.
    """
    if desired == "last_clone":
        if isinstance(value, str) or isinstance(value, Path):
            _HISTORY_CACHE["last_clone"] = str(value)
        else:
            raise TypeError("Invalid type for last_clone")
    else:
        raise ValueError(f"Invalid desired={desired}")
