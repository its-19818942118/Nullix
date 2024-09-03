# nullix/distro/base.py

import concurrent.futures
import subprocess
from abc import ABC, abstractmethod
from typing import List

from nullix.exceptions import PackageInstallationError, PackageUpdateError
from nullix.logging import Logger
from nullix.utils.config_loader import distro_config

logger = Logger().get_logger()


class BaseDistro(ABC):
    """
    Abstract base class for Linux distributions.

    This class defines the interface for distribution-specific package management operations.
    Subclasses should implement the abstract methods to provide distribution-specific functionality.

    Attributes
    ----------
    distro_name : str
        The name of the distribution.
    config : dict
        Configuration dictionary for the distribution.
    package_manager : str
        The name of the package manager used by the distribution.
    install_command : str
        The command used to install packages.
    update_command : str
        The command used to update packages.

    Notes
    -----
    This class serves as a foundation for implementing distribution-specific package management.
    It provides a common interface for package installation and updating across different Linux distributions.

    Key features:
        * ``Abstraction``: Provides a unified interface for package management
        * ``Flexibility``: Allows easy addition of new distributions
        * ``Modularity``: Separates distribution-specific logic from common operations

    See Also
    --------
    ExampleDistro : A concrete implementation example of this abstract base class.

    Examples
    --------
    >>> class UbuntuDistro(BaseDistro):
    ...     def __init__(self):
    ...         super().__init__("ubuntu")
    ...
    ...     def _is_package_available(self, package):
    ...         # Ubuntu-specific implementation
    ...         pass
    """

    def __init__(self, distro_name: str):
        """
        Initialize the BaseDistro instance.

        Parameters
        ----------
        distro_name : str
            The name of the distribution.

        Notes
        -----
        This constructor sets up the basic attributes required for package management operations.
        It retrieves configuration details from the `distro_config` dictionary.

        The initialization process includes:
            1. Setting the distribution name
            2. Loading configuration from `distro_config`
            3. Setting up package manager details

        Raises
        ------
        KeyError
            If the specified `distro_name` is not found in the `distro_config`.
        """
        self.distro_name = distro_name
        self.config = distro_config[distro_name]
        self.package_manager = self.config["package_manager"]
        self.install_command = self.config["install_command"]
        self.update_command = self.config["update_command"]

    @abstractmethod
    def _is_package_available(self, package: str) -> bool:
        """
        Check if a package is available for installation.

        Parameters
        ----------
        package : str
            The name of the package to check.

        Returns
        -------
        bool
            ``True`` if the package is available, ``False`` otherwise.

        Notes
        -----
        This is an abstract method that must be implemented by subclasses.
        It should provide distribution-specific logic to check package availability.

        Implementation considerations:
            * Query the distribution's package database
            * Check online repositories if necessary
            * Handle network errors gracefully
            * Consider caching results for performance

        Raises
        ------
        NotImplementedError
            If the subclass does not implement this method.
        """
        pass

    def install_packages(self, packages: List[str]) -> None:
        """
        Install the given list of packages using parallel processing.

        This method checks package availability in parallel, then installs available packages.

        Parameters
        ----------
        packages : List[str]
            The list of packages to install.

        Raises
        ------
        PackageInstallationError
            If package installation fails.

        Notes
        -----
        This method uses concurrent.futures.ThreadPoolExecutor for parallel processing.
        The installation process follows these steps:

        1. ``Check Availability``: Verify each package's availability in parallel.
        2. ``Filter Packages``: Create a list of available packages.
        3. ``Bulk Installation``: Install all available packages in a single command.

        Performance optimization:
            * ``Parallel checking`` of package availability significantly reduces overall installation time.
            * ``Bulk installation`` minimizes the number of separate package manager invocations.

        Error handling:
            * Logs errors for individual package availability checks
            * Raises a ``PackageInstallationError`` for installation failures

        See Also
        --------
        update_packages : Method for updating installed packages
        """
        logger.info("Starting parallel package installation process...")
        available_packages = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_package = {
                executor.submit(self._is_package_available, package): package
                for package in packages
            }
            for future in concurrent.futures.as_completed(future_to_package):
                package = future_to_package[future]
                try:
                    if future.result():
                        available_packages.append(package)
                except (subprocess.CalledProcessError, OSError) as e:
                    logger.error(
                        "Error checking package availability: %s - %s", package, e
                    )

        if available_packages:
            logger.info("Installing packages: %s", ", ".join(available_packages))
            try:
                cmd = f"{self.install_command} {' '.join(available_packages)}"
                subprocess.run(cmd, shell=True, check=True)
                logger.info(
                    "Packages installed successfully: %s", ", ".join(available_packages)
                )
            except subprocess.CalledProcessError as e:
                error_msg = f"Failed to install packages: {e}"
                logger.error(error_msg)
                raise PackageInstallationError(error_msg) from e
        else:
            logger.warning("No packages to install.")

        logger.info("Package installation process completed.")

    def update_packages(self) -> None:
        """
        Update all installed packages.

        This method runs the update command specified in the distribution configuration.

        Raises
        ------
        PackageUpdateError
            If package update fails.

        Notes
        -----
        The update process involves the following steps:
            1. ``Execute Update Command``: Run the distribution-specific update command.
            2. ``Error Handling``: Catch and log any errors during the update process.
            3. ``Logging``: Record the start and completion of the update process.

        Implementation details:
            * Uses ``subprocess.run`` to execute the update command
            * Runs the command in a shell environment
            * Checks for successful execution and raises an error if the command fails

        See Also
        --------
        install_packages : Method for installing new packages
        """
        logger.info("Starting package update process...")
        try:
            subprocess.run(self.update_command, shell=True, check=True)
            logger.info("Packages updated successfully.")
        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to update packages: {e}"
            logger.error(error_msg)
            raise PackageUpdateError(error_msg) from e
        logger.info("Package update process completed.")


class ExampleDistro(BaseDistro):
    """
    Concrete implementation of BaseDistro for testing purposes.

    This class provides a simple implementation of the BaseDistro abstract class
    for demonstration and testing.

    Notes
    -----
    This example implementation:

    - Always considers packages as available.
    - Logs package installation requests without actual installation.
    - Logs update requests without performing actual updates.

    It's useful for:

    - Testing: Verifying the behavior of the ``BaseDistro`` class.
    - Demonstration: Showing how to implement a concrete subclass of ``BaseDistro``.
    - Dry Runs: Simulating package management operations without affecting the system.

    Warning
    -------
    This is a ``dummy implementation`` and should not be used in production environments.
    """

    def __init__(self):
        """
        Initialize the ExampleDistro instance.

        This constructor calls the parent class constructor with the name "example".

        Notes
        -----
        The "example" name is used to retrieve configuration from the distro_config dictionary.
        Ensure that the distro_config contains an "example" entry for this class to work correctly.
        """
        super().__init__("example")

    def _is_package_available(self, package: str) -> bool:
        """
        Check if a package is available.

        This is a dummy implementation that always returns True.

        Parameters
        ----------
        package : str
            The name of the package to check.

        Returns
        -------
        bool
            Always returns True in this example implementation.

        Notes
        -----
        In a real implementation, this method would typically:
        1. Query the package manager's database.
        2. Check online repositories if necessary.
        3. Return the actual availability status of the package.
        """
        return True

    def install_packages(self, packages: List[str]) -> None:
        """
        Install the given list of packages.

        This is a dummy implementation that only logs the packages to be installed.

        Parameters
        ----------
        packages : List[str]
            The list of packages to install.

        Notes
        -----
        In a real implementation, this method would:
        1. Verify package availability.
        2. Handle dependencies.
        3. Execute the actual installation command.
        4. Verify successful installation.
        """
        logger.info("Installing packages: %s", packages)

    def update_packages(self) -> None:
        """
        Update all installed packages.

        This is a dummy implementation that only logs the update action.

        Notes
        -----
        In a real implementation, this method would:
        1. Check for available updates.
        2. Download updates.
        3. Apply updates to the system.
        4. Handle any post-update tasks or system reconfigurations.
        """
        logger.info("Updating all packages")


if __name__ == "__main__":
    # Test the concrete class
    distro = ExampleDistro()
    distro.install_packages(["example-package"])
    distro.update_packages()
