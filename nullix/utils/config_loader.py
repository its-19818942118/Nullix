# nullix/utils/config_loader.py

import logging
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import BaseModel, ValidationError
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree

from nullix.exceptions import ConfigurationError
from nullix.logging import Logger

console = Console()
logger = Logger().get_logger()


class NullixConfig(BaseModel):
    name: str
    path: str
    git: Dict[str, str]


class DistroConfig(BaseModel):
    package_manager: str
    install_command: str
    update_command: str
    aur_helper: Optional[str] = None
    aur_install_command: Optional[str] = None
    aur_update_command: Optional[str] = None


class DistroConfigs(BaseModel):
    distributions: Dict[str, DistroConfig]


CONFIG_MODELS = {
    "nullix_config.yaml": NullixConfig,
    "distro_configs.yaml": DistroConfigs,
}


def load_yaml_file(file_path: Path) -> Dict[str, Any]:
    """
    Load and parse a YAML file.

    Parameters
    ----------
    file_path : Path
        Path to the YAML file.

    Returns
    -------
    Dict[str, Any]
        Parsed YAML content.

    Raises
    ------
    FileNotFoundError
        If the file is not found.
    yaml.YAMLError
        If there's an error parsing the YAML file.
    """
    logger.info("Loading YAML file: %s", file_path)
    try:
        with open(file_path, "r", encoding="utf-8") as config_file:
            content = yaml.safe_load(config_file)
        logger.info("Successfully loaded YAML file: %s", file_path)
        return content
    except FileNotFoundError:
        logger.error("Configuration file not found: %s", file_path)
        console.print(
            Panel(
                f"[bold red]Error:[/bold red] Configuration file not found: {file_path}",
                title="File Not Found",
            )
        )
        raise
    except yaml.YAMLError as e:
        logger.error("Error parsing YAML configuration file: %s", file_path)
        console.print(
            Panel(
                f"[bold red]Error:[/bold red] Failed to parse YAML file: {file_path}\n{str(e)}",
                title="YAML Parsing Error",
            )
        )
        raise


def validate_config(config: Dict[str, Any], model: BaseModel) -> Dict[str, Any]:
    """
    Validate configuration against a Pydantic model.

    Parameters
    ----------
    config : Dict[str, Any]
        Configuration dictionary to validate.
    model : BaseModel
        Pydantic model to use for validation.

    Returns
    -------
    Dict[str, Any]
        Validated configuration.

    Raises
    ------
    ConfigurationError
        If the configuration is invalid.
    """
    logger.info("Validating configuration against model: %s", model.__name__)
    try:
        validated_config = model(**config).dict()
        logger.info("Configuration validation successful")
        return validated_config
    except ValidationError as e:
        logger.error("Configuration validation failed: %s", e)
        console.print(
            Panel(
                f"[bold red]Error:[/bold red] Invalid configuration:\n{str(e)}",
                title="Validation Error",
            )
        )
        raise ConfigurationError(f"Invalid configuration: {e}") from e


def load_config(config_file_name: str) -> Dict[str, Any]:
    """
    Load and validate a configuration file.

    Parameters
    ----------
    config_file_name : str
        Name of the configuration file to load.

    Returns
    -------
    Dict[str, Any]
        Validated configuration.

    Raises
    ------
    ConfigurationError
        If the configuration file is not supported or invalid.
    """
    logger.info("Loading configuration: %s", config_file_name)
    if config_file_name not in CONFIG_MODELS:
        logger.error("Unsupported configuration file: %s", config_file_name)
        console.print(
            Panel(
                f"[bold red]Error:[/bold red] Unsupported configuration file: {config_file_name}",
                title="Unsupported Config",
            )
        )
        raise ConfigurationError(f"Unsupported configuration file: {config_file_name}")

    config_path = Path(__file__).parent.parent / "config" / config_file_name
    config = load_yaml_file(config_path)
    validated_config = validate_config(config, CONFIG_MODELS[config_file_name])
    logger.info("Successfully loaded and validated configuration: %s", config_file_name)
    return validated_config


# Load configurations
nullix_config = load_config("nullix_config.yaml")
distro_configs = load_config("distro_configs.yaml")


def get_config(config_name: str) -> Dict[str, Any]:
    """
    Get a specific configuration.

    Parameters
    ----------
    config_name : str
        Name of the configuration to retrieve.

    Returns
    -------
    Dict[str, Any]
        The requested configuration.

    Raises
    ------
    ConfigurationError
        If the requested configuration is not found.
    """
    logger.info("Retrieving configuration: %s", config_name)
    configs = {
        "nullix": nullix_config,
        "distro": distro_configs,
    }
    if config_name not in configs:
        logger.error("Unknown configuration: %s", config_name)
        console.print(
            Panel(
                f"[bold red]Error:[/bold red] Unknown configuration: {config_name}",
                title="Config Not Found",
            )
        )
        raise ConfigurationError(f"Unknown configuration: {config_name}")
    logger.info("Successfully retrieved configuration: %s", config_name)
    return configs[config_name]


if __name__ == "__main__":
    console.print(Panel("Nullix Configuration", style="bold green"))

    nullix_tree = Tree("📁 Nullix")
    nullix_tree.add("🏷️ Name: [cyan]" + nullix_config["name"])
    nullix_tree.add("📂 Path: [yellow]" + nullix_config["path"])

    git_branch = nullix_tree.add("🌿 Git")
    git_branch.add("🔗 Repo: [blue]" + nullix_config["git"]["repo"])
    git_branch.add("⚙️ Command: [green]" + nullix_config["git"]["command"])

    console.print(nullix_tree)

    console.print(Panel("Distribution Configurations", style="bold green"))
    distro_table = Table(title="Distribution Configurations")
    distro_table.add_column("Distribution", style="cyan")
    distro_table.add_column("Package Manager", style="magenta")
    distro_table.add_column("Install Command", style="green")
    distro_table.add_column("Update Command", style="yellow")
    distro_table.add_column("AUR Helper", style="blue")
    distro_table.add_column("AUR Install", style="green")
    distro_table.add_column("AUR Update", style="yellow")

    for distro, config in distro_configs["distributions"].items():
        distro_table.add_row(
            distro,
            config["package_manager"],
            config["install_command"],
            config["update_command"],
            config.get("aur_helper", "N/A"),
            config.get("aur_install_command", "N/A"),
            config.get("aur_update_command", "N/A"),
        )

    console.print(distro_table)
