import importlib
import os
from typing import Type

from nullix.distro.base import BaseDistro
from nullix.exceptions import DistroNotSupportedError
from nullix.logging import Logger

logger = Logger().get_logger()


class PluginManager:
    @staticmethod
    def load_custom_distro(distro_name: str) -> Type[BaseDistro]:
        """
        Load a custom distribution class from a plugin.

        Parameters
        ----------
        distro_name : str
            The name of the custom distribution.

        Returns
        -------
        Type[BaseDistro]
            The custom distribution class.

        Raises
        ------
        DistroNotSupportedError
            If the custom distribution plugin is not found or invalid.
        """
        plugin_dir = os.path.join(os.path.dirname(__file__), "plugins")
        plugin_file = os.path.join(plugin_dir, f"{distro_name.lower()}.py")

        if not os.path.exists(plugin_file):
            raise DistroNotSupportedError(
                f"Custom distribution plugin not found: {distro_name}"
            )

        try:
            spec = importlib.util.spec_from_file_location(distro_name, plugin_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            distro_class = getattr(module, distro_name.capitalize())
            if not issubclass(distro_class, BaseDistro):
                raise DistroNotSupportedError(
                    f"Invalid custom distribution class: {distro_name}"
                )

            logger.info("Loaded custom distribution plugin: %s", distro_name)
            return distro_class
        except (AttributeError, ImportError) as e:
            logger.error("Error loading custom distribution plugin: %s", e)
            raise DistroNotSupportedError(
                f"Error loading custom distribution plugin: {distro_name}"
            ) from e
