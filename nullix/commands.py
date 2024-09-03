# nullix/commands.py

import subprocess
from abc import ABC, abstractmethod
from typing import List

from nullix.distro.base import BaseDistro
from nullix.logging import Logger

logger = Logger().get_logger()


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass


class InstallCommand(Command):
    def __init__(self, distro: BaseDistro, packages: List[str]) -> None:
        self.distro = distro
        self.packages = packages

    def execute(self) -> None:
        self.distro.install_packages(self.packages)


class UpdateCommand(Command):
    def __init__(self, distro: BaseDistro) -> None:
        self.distro = distro

    def execute(self) -> None:
        self.distro.update_packages()


class RunCommand(Command):
    def __init__(
        self, command: List[str], shell: bool = False, sudo: bool = False
    ) -> None:
        self.command = command
        self.shell = shell
        self.sudo = sudo

    def execute(self) -> None:
        try:
            if self.sudo:
                self.command.insert(0, "sudo")

            if self.shell:
                cmd = " ".join(self.command)
                subprocess.run(cmd, shell=True, check=True)
            else:
                subprocess.run(self.command, check=True)

            logger.info("Command executed successfully: %s", " ".join(self.command))
        except subprocess.CalledProcessError as e:
            logger.error("Command failed: %s", e)
            raise


class ArchCommands:
    @staticmethod
    def install_base_devel() -> RunCommand:
        return RunCommand(
            ["pacman", "-S", "--needed", "--noconfirm", "git", "base-devel"], sudo=True
        )

    @staticmethod
    def clone_yay() -> RunCommand:
        return RunCommand(["git", "clone", "https://aur.archlinux.org/yay.git"])

    @staticmethod
    def build_yay() -> RunCommand:
        return RunCommand(["makepkg", "-si", "--noconfirm"], shell=True)

    @staticmethod
    def remove_yay_dir() -> RunCommand:
        return RunCommand(["rm", "-rf", "yay"])
