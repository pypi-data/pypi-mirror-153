from pathlib import Path
import typing as t


DEFAULTS_FOLDER: Path = Path(__file__).parent / "defaults"
"""
The path to the default configuration file.
"""


USER_CONFIG_FILE: Path = Path.home() / ".config" / "quickclone.toml"
"""
The path to the user's configuration file.
"""


USER_CACHE_FOLDER: Path = Path.home() / ".cache" / "quickclone"
"""
The path to the cache directory owned by the user to store QuickClone data.
"""

USER_HISTORY_CACHE_FILE: Path = USER_CACHE_FOLDER / "history.toml"
"""
The path to the cache file storing the user's usage history of QuickClone.
"""

CACHE_ITEMS: t.List[str] = ["history.toml"]
"""
List of file names in the cache folder.
"""
