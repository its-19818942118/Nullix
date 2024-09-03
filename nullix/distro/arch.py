# nullix/distro/arch.py

import os
import subprocess
import tempfile
from typing import List, Tuple

from nullix.commands import ArchCommands
from nullix.distro.base import BaseDistro
from nullix.logging import Logger

logger = Logger().get_logger()


class Arch(BaseDistro):
    """
    Arch Linux distribution handler.

    This class manages package installation and updates for Arch Linux,
    including support for AUR packages.

    Attributes
    ----------
    aur_helper : str
        The AUR helper to use (default: 'yay')
    aur_install_command : str
        Command to install AUR packages
    aur_update_command : str
        Command to update AUR packages

    Methods
    -------
    _is_yay_installed()
        Check if yay is installed
    _install_yay()
        Install yay package manager
    _is_package_available(package)
        Check package availability in official repos or AUR
    install_packages(packages)
        Install specified packages
    update_packages()
        Update official and AUR packages
    """

    def __init__(self):
        """
        Initialize the Arch class.

        Sets up the AUR helper and related commands based on the configuration.

        Notes
        -----
        This method initializes the Arch class by calling the parent class
        constructor and setting up AUR-related attributes based on the
        configuration.

        The `aur_helper`, `aur_install_command`, and `aur_update_command`
        are set with default values if not specified in the configuration.
        """
        super().__init__("arch")
        self.aur_helper = self.config.get("aur_helper", "yay")
        self.aur_install_command = self.config.get("aur_install_command", "yay -S")
        self.aur_update_command = self.config.get("aur_update_command", "yay -Syu")

    def _is_yay_installed(self) -> bool:
        """
        Check if the yay package manager is installed on the system.

        Returns
        -------
        bool
            True if yay is installed and can be executed successfully,
            False otherwise.

        Notes
        -----
        This method attempts to run the 'yay --version' command to determine
        if yay is installed and accessible. It catches both
        subprocess.CalledProcessError and FileNotFoundError to handle cases
        where yay is not installed or not in the system PATH.
        """
        try:
            subprocess.run(["yay", "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _install_yay(self) -> None:
        """
        Install the yay package manager on an Arch Linux system.

        Raises
        ------
        subprocess.CalledProcessError
            If any step of the installation process fails.

        Notes
        -----
        This method performs the following steps:
        1. Install base-devel package group
        2. Clone yay repository
        3. Build and install yay

        The installation is performed in a temporary directory, which is
        automatically cleaned up after the installation is complete.

        If the installation fails at any step, an error is logged, and the
        exception is re-raised.
        """
        logger.info("Installing yay...")
        try:
            ArchCommands.install_base_devel().execute()
            with tempfile.TemporaryDirectory() as tmpdir:
                os.chdir(tmpdir)
                ArchCommands.clone_yay().execute()
                os.chdir("yay")
                ArchCommands.build_yay().execute()
            logger.info("yay installed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error("Failed to install yay: %s", e)
            raise
        finally:
            os.chdir(os.path.expanduser("~"))

    def _is_package_available(self, package: str) -> Tuple[bool, str]:
        """
        Check if a specified package is available in the official repositories or AUR.

        Parameters
        ----------
        package : str
            The name of the package to check.

        Returns
        -------
        Tuple[bool, str]
            A tuple containing:
            - bool: True if the package is available, False otherwise
            - str: Source of the package ("official" or "aur")

        Notes
        -----
        The method checks the official repositories first, then the AUR.
        If the package is not found in either, it returns (False, "").
        """
        logger.info("Checking if package '%s' is available...", package)

        # Check in official repositories
        try:
            result = subprocess.run(
                [self.package_manager, "-Ss", "--", package],
                capture_output=True,
                text=True,
                check=True,
            )
            if package in result.stdout:
                logger.info(
                    "Package '%s' is available in official repositories.", package
                )
                return True, "official"
        except subprocess.CalledProcessError:
            pass

        # Check in AUR
        try:
            result = subprocess.run(
                [self.aur_helper, "-Ss", "--", package],
                capture_output=True,
                text=True,
                check=True,
            )
            if package in result.stdout:
                logger.info("Package '%s' is available in AUR.", package)
                return True, "aur"
        except subprocess.CalledProcessError as e:
            logger.error("Error checking AUR for package '%s': %s", package, e)

        logger.info(
            "Package '%s' is not available in official repositories or AUR.", package
        )
        return False, ""

    def install_packages(self, packages: List[str]) -> None:
        """
        Install specified packages using the appropriate package manager.

        This method performs the following steps:
        1. Ensure yay is installed
        2. Categorize input packages into official and AUR packages
        3. Install official packages using system package manager
        4. Install AUR packages using yay

        Parameters
        ----------
        packages : List[str]
            A list of package names to install.

        Raises
        ------
        subprocess.CalledProcessError
            If the installation process fails for either official or AUR packages.

        Notes
        -----
        - Official packages are installed with `sudo` and the `--needed` flag.
        - AUR packages are installed using the configured AUR helper (default: yay).
        - Both installations use the `--noconfirm` flag to avoid prompts.
        """
        logger.info("Starting package installation process...")

        # First, ensure yay is installed
        if not self._is_yay_installed():
            self._install_yay()

        official_packages, aur_packages = [], []

        for package in packages:
            available, repo = self._is_package_available(package)
            if available:
                (official_packages if repo == "official" else aur_packages).append(
                    package
                )

        if official_packages:
            logger.info(
                "Installing official packages: %s", ", ".join(official_packages)
            )
            try:
                cmd = f"sudo {self.install_command} --needed --noconfirm {' '.join(official_packages)}"
                subprocess.run(cmd, shell=True, check=True)
                logger.info(
                    "Official packages installed successfully: %s",
                    ", ".join(official_packages),
                )
            except subprocess.CalledProcessError as e:
                logger.error("Failed to install official packages: %s", e)
                raise

        if aur_packages:
            logger.info("Installing AUR packages: %s", ", ".join(aur_packages))
            try:
                cmd = f"{self.aur_install_command} --needed --noconfirm {' '.join(aur_packages)}"
                subprocess.run(cmd, shell=True, check=True)
                logger.info(
                    "AUR packages installed successfully: %s", ", ".join(aur_packages)
                )
            except subprocess.CalledProcessError as e:
                logger.error("Failed to install AUR packages: %s", e)
                raise

        if not official_packages and not aur_packages:
            logger.warning("No packages to install.")

        logger.info("Package installation process completed.")

    def update_packages(self) -> None:
        """
        Update official and AUR packages.

        This method performs the following steps:
        1. Update official packages using the system's package manager
        2. Update AUR packages using yay (if installed)

        Raises
        ------
        subprocess.CalledProcessError
            If the update process fails for either official or AUR packages.

        Notes
        -----
        - Official packages are updated with `sudo` and the `--noconfirm` flag.
        - AUR packages are updated using the configured AUR helper (default: yay).
        - If yay is not installed, AUR package updates are skipped.
        """
        logger.info("Starting package update process...")
        try:
            # Update official packages
            cmd = f"sudo {self.update_command} --noconfirm"
            subprocess.run(cmd, shell=True, check=True)
            logger.info("Official packages updated successfully.")

            # Update AUR packages if yay is installed
            if self._is_yay_installed():
                cmd = f"{self.aur_update_command} --noconfirm"
                subprocess.run(cmd, shell=True, check=True)
                logger.info("AUR packages updated successfully.")
            else:
                logger.info("yay is not installed. Skipping AUR package updates.")
        except subprocess.CalledProcessError as e:
            logger.error("Failed to update packages: %s", e)
            raise

        logger.info("Package update process completed.")


if __name__ == "__main__":
    # Test the Arch class
    arch = Arch()
    arch.install_packages(["fastfetch", "google-chrome"])
    arch.update_packages()
