# Installing Python Poetry

This guide covers the installation of Poetry, a dependency management and packaging tool for Python, on various Linux distributions.

## Table of Contents

- [Installing Python Poetry](#installing-python-poetry)
  - [Table of Contents](#table-of-contents)
  - [Arch Linux](#arch-linux)
  - [NixOS](#nixos)
  - [Debian-based Distributions](#debian-based-distributions)
  - [Verifying the Installation](#verifying-the-installation)
  - [Additional Resources](#additional-resources)
  - [Installing CLI tool](#installing-cli-tool)
  - [Running CLI tool](#running-cli-tool)

## Arch Linux

On Arch Linux, you can use the `pacman` package manager:

```sh
sudo pacman -S python-poetry
```

## NixOS

For NixOS, use the `nix-env` command:

```sh
nix-env -iA nixpkgs.poetry
```

## Debian-based Distributions

This includes Ubuntu and other Debian derivatives.

1. Install using the official script:

   ```sh
   curl -sSL https://install.python-poetry.org | python3 -
   ```
2. Add Poetry to your PATH by appending this line to your shell configuration file (e.g., `~/.bashrc`, `~/.zshrc`):

   ```sh
   export PATH="$HOME/.local/bin:$PATH"
   ```
3. Reload your shell configuration:

   ```sh
   source ~/.bashrc  # or source ~/.zshrc
   ```

## Verifying the Installation

To confirm that Poetry has been installed correctly, run:

```sh
poetry --version
```

This should display the version of Poetry that has been installed.

## Additional Resources

- [Official Poetry Documentation](https://python-poetry.org/docs/)
- [Poetry GitHub Repository](https://github.com/python-poetry/poetry)

## Installing CLI tool

```sh
poetry install
```

## Running CLI tool

```sh
nullix [COMMAND]
# or
poetry run nullix [COMMAND]
# or with any python version eg:
python -m nullix.distro.arch
```
