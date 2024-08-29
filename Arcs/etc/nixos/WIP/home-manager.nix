{config, pkgs, ... }:

{

  wayland.windowManager.hyprland = {
    # Whether to enable Hyprland wayland compositor
    enable = true;
    # The hyprland package to use
    package = pkgs.hyprland;
    # Whether to enable XWayland
    xwayland.enable = true;
    # Plugins to enable
    plugins = [
      hyprlandPlugins.hyprexpo # Enable HypreXpo
    ];

    # Optional
    # Whether to enable hyprland-session.target on hyprland startup
    systemd.enable = true;
  };

  home = {
    username = "derdelphin";
    homeDirectory = "/home/derdelphin";

    # Enable zsh
    programs.zsh.enable = true;

    # The state version is required and should stay at the version you
    # originally installed.
    home.stateVersion = "24.05";
  }

}
