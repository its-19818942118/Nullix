# nullix/distro/debian.py

import subprocess
from typing import List

from nullix.distro.base import BaseDistro
from nullix.logging import Logger

logger = Logger().get_logger()


class Debian(BaseDistro):
    """
    A class representing the Debian distribution.

    This class inherits from BaseDistro and provides Debian-specific
    functionality for package management.

    Attributes
    ----------
    None

    Methods
    -------
    _is_package_available(package: str) -> bool
        Check if a package is available in the Debian repositories.

    Notes
    -----
    This class assumes that the system it's running on is a Debian-based
    distribution and has access to the apt package management system.

    Examples
    --------
    >>> debian = Debian()
    >>> debian._is_package_available("python3")
    True
    """

    def __init__(self):
        """
        Initialize the Debian class.

        This constructor calls the parent class constructor with "debian"
        as the distribution name.
        """
        super().__init__("debian")

    def _is_package_available(self, package: str) -> bool:
        """
        Check if a package is available in the Debian repositories.

        This method uses the apt-cache command to check if a package
        is available for installation.

        Parameters
        ----------
        package : str
            The name of the package to check.

        Returns
        -------
        bool
            True if the package is available, False otherwise.

        Notes
        -----
        This method captures any CalledProcessError and returns False
        if the apt-cache command fails. This could happen if the package
        cache is not up-to-date or if there are network issues.

        Examples
        --------
        >>> debian = Debian()
        >>> debian._is_package_available("python3")
        True
        >>> debian._is_package_available("non_existent_package")
        False

        See Also
        --------
        subprocess.run : The underlying function used to execute the apt-cache command.
        """
        try:
            result = subprocess.run(
                ["apt-cache", "show", package],
                capture_output=True,
                text=True,
                check=True,
            )
            return bool(result.stdout)
        except subprocess.CalledProcessError:
            logger.warning(f"Failed to check availability of package: {package}")
            return False
