{

  lib,
  host,
  pkgs,
  config,
  username,
  ...

}:

{

  imports = [

    # ~ ==== Import Packages ==== ~ #
    ./pkgs/user-pkgs.nix
    ./pkgs/system-pkgs.nix

    # ~ ==== Import Configurations ==== ~ #
    ./configs/users.nix
    ./configs/fonts.nix
    ./configs/default.nix
    ./configs/programs.nix
    ./configs/security.nix
    ./configs/services.nix
    ./configs/environment.nix
    ./configs/filesystems.nix
    ./configs/system-configuration.nix

    # ~ ==== Import Hardware Configurations ==== ~ #
    ./configs/bootloader.nix
    ./hardware/hardware-configuration.nix
    ./hardware/user-hardware-configuration.nix
    ./hardware/nvidia.nix

  ];

  # ===== System Version =====
  system.stateVersion = "24.11"; # Don't change this

}
