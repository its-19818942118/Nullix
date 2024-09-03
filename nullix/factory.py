# nullix/factory.py

from abc import ABC, abstractmethod

from nullix.distro.arch import Arch
from nullix.distro.base import BaseDistro
from nullix.distro.debian import Debian
from nullix.distro.nixos import NixOS
from nullix.exceptions import DistroNotSupportedError


class DistroFactory(ABC):
    """
    Abstract base class for distribution factories.

    This class defines the interface for creating distribution objects.
    """

    @abstractmethod
    def create_distro(self) -> BaseDistro:
        """
        Create and return a distribution object.

        Returns
        -------
        BaseDistro
            An instance of a specific distribution class.
        """


class NixOSFactory(DistroFactory):
    """Factory class for creating NixOS distribution objects."""

    def create_distro(self) -> BaseDistro:
        """
        Create and return a NixOS distribution object.

        Returns
        -------
        BaseDistro
            An instance of the NixOS class.
        """
        return NixOS()


class ArchFactory(DistroFactory):
    """Factory class for creating Arch Linux distribution objects."""

    def create_distro(self) -> BaseDistro:
        """
        Create and return an Arch Linux distribution object.

        Returns
        -------
        BaseDistro
            An instance of the Arch class.
        """
        return Arch()


class DebianFactory(DistroFactory):
    """Factory class for creating Debian distribution objects."""

    def create_distro(self) -> BaseDistro:
        """
        Create and return a Debian distribution object.

        Returns
        -------
        BaseDistro
            An instance of the Debian class.
        """
        return Debian()


class DistroFactoryProducer:
    """Class for producing the appropriate distribution factory."""

    @staticmethod
    def get_factory(distro_name: str) -> DistroFactory:
        """
        Get the appropriate distribution factory based on the distribution name.

        Parameters
        ----------
        distro_name : str
            The name of the distribution.

        Returns
        -------
        DistroFactory
            An instance of the appropriate distribution factory.

        Raises
        ------
        DistroNotSupportedError
            If the specified distribution is not supported.
        """
        if distro_name == "nixos":
            return NixOSFactory()
        elif distro_name == "arch":
            return ArchFactory()
        elif distro_name in ["debian", "ubuntu"]:
            return DebianFactory()
        else:
            raise DistroNotSupportedError(f"Unsupported distribution: {distro_name}")
