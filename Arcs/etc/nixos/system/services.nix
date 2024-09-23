{
  lib,
  pkgs,
  config,
  inputs,
  system,
  ...
}:

{
  # Services
  services = {
    # Enable EnvFS
    envfs.enable = true;

    # Fix USB sticks not mounting or being listed
    devmon.enable = true;
    udisks2.enable = true;
    gvfs.enable = true;

    # xserver stuff
    xserver = {
      # Enable the X11 windowing system.
      # You can disable this if you're only using the Wayland session.
      enable = true;

      # Configure keymap in X11
      xkb = {
        layout = "de";
        variant = "";
      };
    };

    # Enable touchpad support (enabled default in most desktopManager).
    libinput = {
      enable = true;
    };

    # Enable SDDM Display Manager.
    displayManager.sddm.enable = true;

    # Printing support
    printing = {
      enable = true;
    };

    # DBus
    dbus.enable = true;

    # Locate
    locate = {
      enable = true;
    };

    # Enable the OpenSSH daemon
    openssh = {
      enable = true;
    };

    # Sound
    # hardware.pulseaudio.enable = false;
    pipewire = {
      enable = true;
      alsa = {
        enable = true;
        support32Bit = true;
      };
      pulse.enable = true;
      wireplumber.enable = true;
      # If you want to use JACK applications, uncomment this
      jack.enable = true;
    };
  };

  # Hardware
  # hardware.enableAllFirmware = true;
  hardware.bluetooth = {
    enable = true;
    powerOnBoot = true;
  };

  # Enable networking
  # networking.networkmanager.enable = true;

  # Enable SysRQ
  # boot.kernel.sysctl."kernel.sysrq" = 1;

  # XDG Desktop Portal stuff
  xdg.portal = {
    enable = true;
    wlr.enable = true;
    config.common.default = "*";
    extraPortals = [ pkgs.xdg-desktop-portal-gtk ];
  };

  # Security
  security = {
    rtkit.enable = true;
    polkit.enable = true;
  };
  # Polkit
  systemd = {
    user.services.polkit-gnome-authentication-agent-1 = {
      description = "polkit-gnome-authentication-agent-1";
      wantedBy = [ "graphical-session.target" ];
      wants = [ "graphical-session.target" ];
      after = [ "graphical-session.target" ];
      serviceConfig = {
        Type = "simple";
        ExecStart = "${pkgs.polkit_gnome}/libexec/polkit-gnome-authentication-agent-1";
        Restart = "on-failure";
        RestartSec = 1;
        TimeoutStopSec = 10;
      };
    };
  };

  # security.polkit.extraConfig = ''
  #  polkit.addRule(function(action, subject) {
  #    if (
  #      subject.isInGroup("users")
  #        && (
  #          action.id == "org.freedesktop.login1.reboot" ||
  #          action.id == "org.freedesktop.login1.reboot-multiple-sessions" ||
  #          action.id == "org.freedesktop.login1.power-off" ||
  #          action.id == "org.freedesktop.login1.power-off-multiple-sessions"
  #        )
  #      )
  #    {
  #      return polkit.Result.YES;
  #    }
  #  })
  # '';

  # Some programs need SUID wrappers, can be configured further or are
  # started in user sessions.
  # programs.mtr.enable = true;
  programs.gnupg.agent = {
    enable = true;
    enableSSHSupport = true;
  };
}
