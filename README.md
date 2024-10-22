# Nullix

This repository contains a NixOS configuration for setting up a desktop environment using dotfiles for Hyprland

## Features

- NixOS configuration with Hyprland as the primary window manager
- Home-manager integration for user-specific configurations
- Support for both regular installation and VM creation
- Customizable user, git, and host settings

## Prerequisites

- NixOS installed on your system
- Basic understanding of Nix and NixOS configuration
- git (`nix-shell -p git`)

## Getting Started

1. Clone this repository:
   ```
   git clone https://github.com/its-19818942118/Nullix.git
   ```

2. Edit the `flake.nix` file to set your username, git information, and host name:
   ```nix
   username = "your-username";
   gitUser = "Your Name";
   gitEmail = "your.email@example.com";
   host = "your-hostname";
   ```

3. Update the `defaultPassword` in `flake.nix` (you should change this after first boot using passwd):
   ```nix
   defaultPassword = "your-secure-password";
   ```

4. Customize the configuration files as needed:
   - `configuration.nix`: System-wide settings
   - `home.nix`: User-specific configurations
   - `hardware-configuration.nix`: Hardware-specific settings (auto-generated)

5. Build and switch to the new configuration:
   ```
   sudo nixos-rebuild switch --flake .#nullix
   ```

## VM Creation

To create a VM with this configuration:

   ```
   nix run .
   ```

## Customization

- Add or remove packages in `configuration.nix` and `home.nix`
- Modify Hyprland and other application configs in the respective files
- Add custom modules in the `modules/` directory


## TODO:
 
- [ ] base nixos config
- [ ] import dotfiles
- [ ] set home.file for managed dotfiles
- [ ] custom params for home manager

## License

This project is open source and available under the [MIT License](LICENSE).

