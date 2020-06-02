import bpy
from typing import Union
from pathlib import Path


def beautify(text: str) -> str:
    return ' '.join(w.capitalize() for w in text.split('_'))


def description(*args: str) -> str:
    return '.\n'.join(args)


def resolve(path: Union[str, Path]) -> Path:
    return Path(path).resolve()


def sanitize(path: Union[str, Path]) -> Path:
    path = resolve(path)
    drive = path.drive

    path = str(path)[len(drive):]
    path = ''.join('_' if c in ':*?"<>|' else c for c in path)

    return Path.joinpath(drive, path)


def open_folder(path: Union[str, Path]) -> bool:
    try:
        bpy.ops.wm.url_open(url=resolve(path).as_uri())
        return True

    except:
        print('Failed to open folder')
        return False
