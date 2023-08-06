# Need to be sure that we dont import anything which may lead to circular imports
import pickle
from pathlib import Path
from typing import Any, List, Optional, Type


def isinstanceany(obj: Any, class_list: List[Type]) -> bool:
    for cls in class_list:
        if isinstance(obj, cls):
            return True
    return False


def unpickle_object_from_file(
    file_path: Path, verify_class: Optional[Any] = None
) -> Any:
    """Reads the contents of file_path and unpickles the binary content into an object.
    If verify_class is provided, checks if the object is an instance of that class.
    """
    from phiterm.utils.log import logger

    _obj = None
    # logger.debug(f"Reading {file_path}")
    if file_path.exists() and file_path.is_file():
        _obj = pickle.load(file_path.open("rb"))

    # if verify_class is not None:
    #     logger.debug(f"Verifying if obj matches {verify_class}")

    if _obj and verify_class and not isinstance(_obj, verify_class):
        logger.error(f"Unpickled object does not match {verify_class}")
        _obj = None

    return _obj


def pickle_object_to_file(obj: Any, file_path: Path) -> Any:
    """Pickles and saves object to file_path"""

    _obj_parent = file_path.parent
    if not _obj_parent.exists():
        _obj_parent.mkdir(parents=True, exist_ok=True)
    pickle.dump(obj, file_path.open("wb"))


def str_to_int(inp: str) -> Optional[int]:
    """
    Safely converts a string value to integer.
    Args:
        inp: input string

    Returns: input string as int if possible, None if not
    """
    try:
        val = int(inp)
        return val
    except Exception:
        return None


def is_empty(val: Any) -> bool:
    if val is None or len(val) == 0 or val == "":
        return True
    return False
