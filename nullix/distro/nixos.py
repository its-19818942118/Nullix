# nullix/distro/nixos.py

import subprocess
from typing import List

from nullix.distro.base import BaseDistro
from nullix.logging import Logger

logger = Logger().get_logger()


class NixOS(BaseDistro):
    """
    A class representing the NixOS distribution, inheriting from BaseDistro.

    This class provides methods for package management specific to NixOS,
    including package installation, updating, and querying package availability.

    Attributes
    ----------
    None

    Methods
    -------
    _is_package_available(package)
        Check if a package is available in the Nix channels.
    install_packages(packages)
        Install a list of packages using Nix.
    update_packages()
        Update all installed packages using Nix.
    get_package_manager()
        Get the name of the package manager.
    get_install_command()
        Get the command for installing packages.
    get_update_command()
        Get the command for updating packages.
    """

    def __init__(self):
        """
        Initialize the NixOS class.

        Calls the parent class constructor with "nixos" as the distro name.
        """
        super().__init__("nixos")

    def _is_package_available(self, package: str) -> bool:
        """
        Check if a package is available in the Nix channels.

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
        This method uses the `nix-env -qa` command to query available packages.
        It captures the output and checks if it's non-empty to determine availability.

        Raises
        ------
        subprocess.CalledProcessError
            If the subprocess call to `nix-env -qa` fails.
        """
        try:
            result = subprocess.run(
                ["nix-env", "-qa", package], capture_output=True, text=True, check=True
            )
            return bool(result.stdout)
        except subprocess.CalledProcessError:
            return False

    def install_packages(self, packages: List[str]) -> None:
        """
        Install the given list of packages using Nix.

        This method checks package availability, installs available packages,
        and logs the process.

        Parameters
        ----------
        packages : List[str]
            The list of packages to install.

        Returns
        -------
        None

        Notes
        -----
        - Unavailable packages are skipped and logged as warnings.
        - The installation process uses the `nix-env -iA` command.
        - The method logs the start and completion of the installation process.

        Raises
        ------
        subprocess.CalledProcessError
            If the package installation process fails.
        """
        logger.info("Starting package installation process...")
        available_packages = []

        for package in packages:
            if self._is_package_available(package):
                available_packages.append(package)
            else:
                logger.warning(
                    "Package '%s' is not available in the Nix channels.", package
                )

        if available_packages:
            logger.info("Installing packages: %s", ", ".join(available_packages))
            try:
                subprocess.run(["nix-env", "-iA"] + available_packages, check=True)
                logger.info(
                    "Packages installed successfully: %s", ", ".join(available_packages)
                )
            except subprocess.CalledProcessError as e:
                logger.error("Failed to install packages: %s", e)
        else:
            logger.warning("No packages to install.")

        logger.info("Package installation process completed.")

    def update_packages(self) -> None:
        """
        Update all installed packages using Nix.

        This method updates Nix channels and upgrades all installed packages.

        Returns
        -------
        None

        Notes
        -----
        The update process involves two steps:
        1. Updating Nix channels using `nix-channel --update`
        2. Upgrading installed packages using `nix-env --upgrade`

        The method logs the start and completion of the update process.

        Raises
        ------
        subprocess.CalledProcessError
            If either the channel update or package upgrade process fails.
        """
        logger.info("Starting package update process...")
        try:
            subprocess.run(["nix-channel", "--update"], check=True)
            subprocess.run(["nix-env", "--upgrade"], check=True)
            logger.info("Packages updated successfully.")
        except subprocess.CalledProcessError as e:
            logger.error("Failed to update packages: %s", e)
        logger.info("Package update process completed.")

    def get_package_manager(self) -> str:
        """
        Get the name of the package manager.

        Returns
        -------
        str
            The name of the package manager (nix).

        Notes
        -----
        This method is used to identify the package manager used by NixOS.
        """
        return "nix"

    def get_install_command(self) -> str:
        """
        Get the command for installing packages.

        Returns
        -------
        str
            The command to install packages using Nix.

        Notes
        -----
        The returned command is `nix-env -iA`, which installs packages
        from the Nix channels. This command is specific to NixOS and
        differs from other package managers.
        """
        return "nix-env -iA"

    def get_update_command(self) -> str:
        """
        Get the command for updating packages.

        Returns
        -------
        str
            The command to update Nix channels and upgrade packages.

        Notes
        -----
        The returned command combines two operations:
        1. `nix-channel --update`: Updates the Nix channels
        2. `nix-env -u`: Upgrades all installed packages

        This combined command ensures both the channels and packages are updated.
        """
        return "nix-channel --update && nix-env -u"


if __name__ == "__main__":
    # Test the NixOS class
    nixos = NixOS()
    nixos.install_packages(["fastfetch"])
    nixos.update_packages()
