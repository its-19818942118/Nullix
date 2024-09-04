# nullix/utils/read_packages.py

import re
from typing import List

import click

from nullix.logging import Logger

logger = Logger().get_logger()


def read_packages_from_file(file_path: str) -> List[str]:
    """
    Read packages from a file, ignoring empty lines and comments.

    Parameters
    ----------
    file_path : str
        The path to the file containing package names.

    Returns
    -------
    List[str]
        A list of package names read from the file.

    Raises
    ------
    click.FileError
        If the specified file is not found.

    Notes
    -----
    This function reads package names from a file, handling both regular package
    lists and requirements.txt format. It ignores empty lines and comments
    (lines starting with '#').

    For requirements.txt files, it extracts only the package name, ignoring
    version specifiers or other constraints.

    Examples
    --------
    >>> packages = read_packages_from_file('package_list.txt')
    >>> print(packages)
    ['neofetch', 'htop', 'neovim']
    """
    packages = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if file_path.endswith("requirements.txt"):
                        # Extract package name from requirements.txt format
                        match = re.match(r"^([a-zA-Z0-9_-]+)", line)
                        if match:
                            packages.append(match.group(1))
                    else:
                        packages.append(line)
    except FileNotFoundError as exc:
        logger.error("Package list file not found: %s", file_path)
        raise click.FileError(file_path, hint="Make sure the file exists.") from exc
    return packages
