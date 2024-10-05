{

  lib,
  host,
  pkgs,
  config,
  username,
  ...

}:

{

  # ~ ===== System Services ===== ~ #
  services = {
    libinput.enable = true;
    spice-vdagentd.enable = true;
    qemuGuest.enable = true;
    blueman.enable = true;
    pipewire = {
      enable = true;
      alsa = {
        enable = true;
        support32Bit = true;
      };
      pulse.enable = true;
      wireplumber.enable = true;
    };
    dbus.enable = true;
    xserver = {
      enable = false;
      videoDrivers = [ "nvidia" ];
    };
    openssh.enable = true;
    displayManager = {
      sddm = {
        enable = true;
        wayland.enable = true;
        settings = {
          autoLogin.enable = true;
          autoLogin.user = username;
          AutoLogin = {
            User = username;
            Session = "hyprland.desktop";
          };
        };
        theme = "catppuccin-mocha";
        package = pkgs.kdePackages.sddm;
      };
      sessionPackages = [ pkgs.hyprland ];
    };
  };

  networking = {
    hostName = host;
    networkmanager.enable = true;
  };
  networking.firewall = {
    enable = true;
    allowedTCPPorts = [
      # SSH
      22
      # Pipewire
      4713
    ];
    allowedUDPPorts = [
      # Pipewire
      4713
      # DHCP
      68
      546
    ];
  };

}
