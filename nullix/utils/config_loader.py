# nullix/utils/config_loader.py

from pathlib import Path
from typing import Any, Dict

import yaml

from nullix.exceptions import ConfigurationError
from nullix.logging import Logger

logger = Logger().get_logger()


def load_distro_config() -> Dict[str, Any]:
    """
    Load distribution configurations from a YAML file.

    This function reads the distribution configurations from a YAML file
    located at 'nullix/config/distro_configs.yaml'. It validates the
    configuration to ensure all required keys are present for each
    distribution.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing the distribution configurations.
        The structure is:
        {
            'distro_name': {
                'package_manager': str,
                'install_command': str,
                'update_command': str,
                ...
            },
            ...
        }

    Raises
    ------
    ConfigurationError
        If the configuration file is missing required keys for any distribution.
    FileNotFoundError
        If the configuration file is not found at the expected location.
    yaml.YAMLError
        If there's an error parsing the YAML file.
    KeyError
        If the 'distributions' key is not found in the YAML file.

    Notes
    -----
    The function expects the YAML file to have a 'distributions' key at the
    top level, under which each distribution's configuration is defined.

    Required keys for each distribution are:
    - package_manager
    - install_command
    - update_command

    Example
    -------
    >>> config = load_distro_config()
    >>> print(config['ubuntu']['package_manager'])
    'apt'
    """
    config_path = Path(__file__).parent.parent / "config" / "distro_configs.yaml"
    try:
        with open(config_path, "r", encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)["distributions"]

        required_keys = ["package_manager", "install_command", "update_command"]
        for distro, distro_conf in config.items():
            missing_keys = [key for key in required_keys if key not in distro_conf]
            if missing_keys:
                raise ConfigurationError(
                    f"Missing required keys for {distro}: {', '.join(missing_keys)}"
                )

        return config
    except FileNotFoundError:
        logger.error("Configuration file not found: %s", config_path)
        raise
    except yaml.YAMLError:
        logger.error("Error parsing YAML configuration file: %s", config_path)
        raise
    except KeyError as exc:
        logger.error("Invalid configuration structure: 'distributions' key not found")
        raise ConfigurationError("Invalid configuration structure") from exc


distro_config = load_distro_config()
