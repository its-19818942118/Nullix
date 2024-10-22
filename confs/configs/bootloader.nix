
{
  
  lib,
  pkgs,
  config,
  ...
  
}:

{
  
  # ~ ===== Boot Configuration ===== ~ #
  boot.loader.systemd-boot.enable = true;
  boot.kernelPackages = pkgs.linuxPackages_zen;

  # #! Enable grub below, note you will have to change to the new bios boot option for settings to apply
  # boot = {
    
  #   loader = {
      
  #     efi.canTouchEfiVariables = true;
  #     grub = {
        
  #       enable = true;
  #       device = "nodev";
  #       efiSupport = true;
  #       useOSProber = true;
        
  #     };
      
  #   };
    
  # };
  
}
