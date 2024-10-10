{

  lib,
  pkgs,
  config,
  ...

}:

{

  # ~ ===== Boot Configuration ===== ~ #
  boot = {

    loader = {

      efi = {

        canTouchEfiVariables = true;

      };

      systemd-boot = {

        enable = true;

      };

      #! Enable grub below, note you will have to change to the new bios boot option for settings to apply
      #! You can keep systemd boot if you want to, we recommend grub for multiboot with windows
      # grub = {

      #   enable = true;
      #   devices = [ "nodev" ];
      #   efiSupport = true;
      #   useOSProber = true;

      # };

    };

    kernelPackages = pkgs.linuxPackages_zen;

  };

}
