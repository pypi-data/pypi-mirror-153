# SPDX-FileCopyrightText: Copyright 2022, Arm Limited and/or its affiliates.
# SPDX-License-Identifier: Apache-2.0
"""Module to host all file system related functions."""
import importlib.resources as pkg_resources
import re
import shutil
from pathlib import Path
from typing import Any
from typing import Literal
from typing import Optional

ResourceType = Literal["applications", "systems", "tools"]


def get_aiet_resources() -> Path:
    """Get resources folder path."""
    with pkg_resources.path("aiet", "__init__.py") as init_path:
        project_root = init_path.parent
        return project_root / "resources"


def get_resources(name: ResourceType) -> Path:
    """Return the absolute path of the specified resource.

    It uses importlib to return resources packaged with MANIFEST.in.
    """
    if not name:
        raise ResourceWarning("Resource name is not provided")

    resource_path = get_aiet_resources() / name
    if resource_path.is_dir():
        return resource_path

    raise ResourceWarning("Resource '{}' not found.".format(name))


def copy_directory_content(source: Path, destination: Path) -> None:
    """Copy content of the source directory into destination directory."""
    for item in source.iterdir():
        src = source / item.name
        dest = destination / item.name

        if src.is_dir():
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)


def remove_resource(resource_directory: str, resource_type: ResourceType) -> None:
    """Remove resource data."""
    resources = get_resources(resource_type)

    resource_location = resources / resource_directory
    if not resource_location.exists():
        raise Exception("Resource {} does not exist".format(resource_directory))

    if not resource_location.is_dir():
        raise Exception("Wrong resource {}".format(resource_directory))

    shutil.rmtree(resource_location)


def remove_directory(directory_path: Optional[Path]) -> None:
    """Remove directory."""
    if not directory_path or not directory_path.is_dir():
        raise Exception("No directory path provided")

    shutil.rmtree(directory_path)


def recreate_directory(directory_path: Optional[Path]) -> None:
    """Recreate directory."""
    if not directory_path:
        raise Exception("No directory path provided")

    if directory_path.exists() and not directory_path.is_dir():
        raise Exception(
            "Path {} does exist and it is not a directory".format(str(directory_path))
        )

    if directory_path.is_dir():
        remove_directory(directory_path)

    directory_path.mkdir()


def read_file(file_path: Path, mode: Optional[str] = None) -> Any:
    """Read file as string or bytearray."""
    if file_path.is_file():
        if mode is not None:
            # Ignore pylint warning because mode can be 'binary' as well which
            # is not compatible with specifying encodings.
            with open(file_path, mode) as file:  # pylint: disable=unspecified-encoding
                return file.read()
        else:
            with open(file_path, encoding="utf-8") as file:
                return file.read()

    if mode == "rb":
        return b""
    return ""


def read_file_as_string(file_path: Path) -> str:
    """Read file as string."""
    return str(read_file(file_path))


def read_file_as_bytearray(file_path: Path) -> bytearray:
    """Read a file as bytearray."""
    return bytearray(read_file(file_path, mode="rb"))


def valid_for_filename(value: str, replacement: str = "") -> str:
    """Replace non alpha numeric characters."""
    return re.sub(r"[^\w.]", replacement, value, flags=re.ASCII)
