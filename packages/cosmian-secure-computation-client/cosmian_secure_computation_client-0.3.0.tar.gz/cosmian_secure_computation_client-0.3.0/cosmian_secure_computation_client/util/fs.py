"""cosmian_secure_computation_client.util.fs module."""

from pathlib import Path
import tarfile
from typing import Iterator


def is_hidden(path: Path) -> bool:
    return any((part.startswith(".") for part in path.parts))


def ls(dir_path: Path, dot_files: bool = False) -> Iterator[Path]:
    for path in sorted(dir_path.absolute().rglob("*")):  # type: Path
        if path.is_file():
            if not dot_files and not is_hidden(path.relative_to(dir_path)):
                yield path


def tar(dir_path: Path, tar_path: Path, dot_files: bool = False) -> Path:
    with tarfile.open(tar_path, "w:") as tar_file:
        for path in ls(dir_path, dot_files):
            rel_path: Path = path.relative_to(dir_path)
            tar_file.add(path, rel_path)

    return tar_path
