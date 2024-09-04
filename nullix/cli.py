# nullix/cli.py

import os
import subprocess
from typing import List, Optional

import click
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree

from nullix.exceptions import PackageInstallationError, PackageUpdateError
from nullix.installer import Installer
from nullix.logging import Logger
from nullix.utils.detector import DistroDetector
from nullix.utils.read_packages import read_packages_from_file

console = Console()
logger = Logger().get_logger()


def print_fancy_header():
    rprint(
        Panel.fit(
            "[bold cyan]Nullix[/bold cyan]\n"
            "[italic]A versatile package management tool for various Linux distributions[/italic]",
            border_style="bold green",
            padding=(1, 1),
        )
    )


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    """
    Nullix: A versatile package management tool for various Linux distributions.

    This CLI tool provides a unified interface for package management across
    different Linux distributions. It supports operations such as package
    installation, system updates, and distribution detection.

    Usage:
      nullix [OPTIONS] COMMAND [ARGS]...

    Commands:
      install   Install specified packages or packages from a file.
      update    Update all installed packages on the system.
      detect    Detect and display the current Linux distribution.

    For more information on a specific command, use:
      nullix COMMAND --help
    """
    print_fancy_header()
    ctx.obj = Installer(DistroDetector())


@cli.command()
@click.argument("packages", nargs=-1)
@click.option(
    "--file",
    "-f",
    type=click.Path(exists=True),
    help="Path to a file containing package names.",
)
@click.pass_obj
def install(installer: Installer, packages: List[str], file: Optional[str]) -> None:
    """
    Install specified packages or packages from a file.

    This command allows you to install packages either by specifying them
    directly as arguments or by providing a file containing package names.

    If no packages are specified and no file is provided, the command will
    attempt to use a default 'packages.txt' file in the 'packages' directory.

    Usage:
      nullix install [OPTIONS] [PACKAGES]...

    Arguments:
      PACKAGES  Names of packages to install (space-separated).

    Options:
      -f, --file PATH  Path to a file containing package names (one per line).
      --help           Show this message and exit.

    Examples:
      nullix install neofetch htop
      nullix install -f ~/my_packages.txt
    """
    if not packages and not file:
        default_file = os.path.join(
            os.path.dirname(__file__), "packages", "packages.txt"
        )
        if os.path.exists(default_file):
            packages = read_packages_from_file(default_file)
        else:
            logger.error("No packages specified and default packages.txt not found.")
            raise click.UsageError(
                "Please specify packages to install or provide a package list file."
            )
    elif file:
        packages = read_packages_from_file(file)

    if not packages:
        logger.warning("No packages to install.")
        return

    with console.status("[bold green]Installing packages...") as status:
        try:
            installer.install_packages(list(packages))
            status.update("[bold green]Installation complete!")

            table = Table(title="Installed Packages")
            table.add_column("Package", style="cyan")
            table.add_column("Status", style="green")

            for package in packages:
                table.add_row(package, "Installed")

            console.print(table)

        except (PackageInstallationError, subprocess.CalledProcessError) as e:
            status.update("[bold red]Installation failed!")
            logger.error("Installation failed: %s", str(e))
            rprint(
                Panel(
                    f"[red]Installation failed.[/red]\n{str(e)}",
                    title="Error",
                    expand=False,
                )
            )


@cli.command()
@click.pass_obj
def update(installer: Installer) -> None:
    """
    Update all installed packages on the system.

    This command updates all installed packages using the appropriate
    package manager for the detected Linux distribution.

    Usage:
      nullix update

    Options:
      --help  Show this message and exit.

    Example:
      nullix update
    """
    with console.status("[bold green]Updating packages...") as status:
        try:
            installer.update_packages()
            status.update("[bold green]Update complete!")
            rprint(
                Panel(
                    "[green]All packages have been successfully updated.[/green]",
                    title="Update Status",
                    expand=False,
                )
            )
        except PackageUpdateError as e:
            status.update("[bold red]Update failed!")
            logger.error(str(e))
            rprint(
                Panel(
                    f"[red]Update failed.[/red]\n{str(e)}", title="Error", expand=False
                )
            )


@cli.command()
@click.pass_obj
def detect(installer: Installer) -> None:
    """
    Detect and display the current Linux distribution.

    This command identifies the Linux distribution currently running on the
    system and displays the information.

    Usage:
      nullix detect

    Options:
      --help  Show this message and exit.

    Example:
      nullix detect
    """
    distro_name = installer.distro.__class__.__name__
    rprint(
        Panel(
            f"[bold cyan]Detected distribution:[/bold cyan] [green]{distro_name}[/green]",
            title="Distribution Info",
            expand=False,
            border_style="cyan",
        )
    )


def print_help():
    tree = Tree("[bold cyan]Nullix Commands[/bold cyan]")
    tree.add("[bold green]install[/bold green] - Install packages")
    tree.add("[bold yellow]update[/bold yellow] - Update all packages")
    tree.add("[bold magenta]detect[/bold magenta] - Detect Linux distribution")

    usage = Syntax(
        "nullix [OPTIONS] COMMAND [ARGS]...",
        "bash",
        theme="monokai",
        word_wrap=True,
    )

    rprint(
        Panel(
            f"{tree}\n\n[bold]Usage:[/bold]\n{usage}",
            title="Nullix Help",
            expand=False,
            border_style="green",
        )
    )


if __name__ == "__main__":
    cli.add_command(print_help, name="help")
    cli()
