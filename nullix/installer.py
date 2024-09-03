# nullix/installer.py

from pathlib import Path
from typing import List

from nullix.exceptions import PackageInstallationError, PackageUpdateError
from nullix.factory import DistroFactoryProducer
from nullix.logging import Logger
from nullix.utils.detector import DistroDetector

logger = Logger().get_logger()


class Installer:
    """
    Installer class to handle package installation and updates.

    This class provides methods for installing packages and updating the system
    based on the detected Linux distribution.

    Parameters
    ----------
    detector : DistroDetector
        An instance of DistroDetector to detect the current distribution.

    Attributes
    ----------
    detector : DistroDetector
        The DistroDetector instance used for distribution detection.
    distro : BaseDistro
        An instance of the detected distribution class.

    Methods
    -------
    install_packages(packages: List[str]) -> None
        Install the given list of packages.
    update_packages() -> None
        Update all installed packages.
    install_from_file(file_path: str) -> None
        Install packages listed in a file.
    """

    def __init__(self, detector: DistroDetector) -> None:
        """
        Initialize the Installer instance.

        Parameters
        ----------
        detector : DistroDetector
            An instance of DistroDetector to detect the current distribution.
        """
        self.detector: DistroDetector = detector
        distro_name = self.detector.detect()
        logger.info("Detected distribution: %s", distro_name)
        factory = DistroFactoryProducer.get_factory(distro_name)
        self.distro = factory.create_distro()
        logger.info("Created distro instance: %s", self.distro.__class__.__name__)

    def install_packages(self, packages: List[str]) -> None:
        """
        Install the given list of packages.

        Parameters
        ----------
        packages : List[str]
            The list of packages to install.

        Raises
        ------
        PackageInstallationError
            If package installation fails.
        """
        logger.info("Attempting to install packages: %s", ", ".join(packages))
        try:
            self.distro.install_packages(packages)
            logger.info("Successfully installed packages: %s", ", ".join(packages))
        except Exception as e:
            logger.error("Failed to install packages: %s", e)
            raise PackageInstallationError(f"Failed to install packages: {e}") from e

    def update_packages(self) -> None:
        """
        Update all installed packages.

        This method attempts to update all packages installed on the system
        using the appropriate package manager for the detected distribution.

        Raises
        ------
        PackageUpdateError
            If the package update process fails for any reason.

        Notes
        -----
        The method uses the distribution-specific update command
        implemented in the `self.distro.update_packages()` method.

        If an exception occurs during the update process, it is caught,
        logged, and then re-raised as a `PackageUpdateError` with the
        original exception chained.
        """
        logger.info("Attempting to update all packages")
        try:
            self.distro.update_packages()
            logger.info("Successfully updated all packages")
        except Exception as e:
            logger.error("Failed to update packages: %s", e)
            raise PackageUpdateError(f"Failed to update packages: {e}") from e

    def install_from_file(self, file_path: str) -> None:
        """
        Install packages listed in a file.

        Parameters
        ----------
        file_path : str
            The path to the file containing the list of packages.

        Raises
        ------
        FileNotFoundError
            If the specified file is not found.
        """
        logger.info("Attempting to install packages from file: %s", file_path)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                packages = [line.strip() for line in f if line.strip()]
            logger.info("Read %d packages from file", len(packages))
            self.install_packages(packages)
        except FileNotFoundError:
            logger.error("Package list file not found: %s", file_path)
            raise


if __name__ == "__main__":
    installer = Installer(DistroDetector())
    try:
        # Get the directory of the current script
        script_dir = Path(__file__).resolve().parent
        # Construct the path to the packages file
        packages_file = script_dir / "packages" / "packages.txt"

        logger.info("Looking for packages file at: %s", packages_file)

        if packages_file.exists():
            installer.install_from_file(str(packages_file))
            installer.update_packages()
        else:
            logger.error("Packages file not found: %s", packages_file)
    except Exception as ex:
        logger.error("An error occurred: %s", str(ex))
