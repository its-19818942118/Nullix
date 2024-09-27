{
  lib,
  pkgs,
  config,
  gitUser,
  gitEmail,
  username,
  ...
}:

{
  
  home.username = username;
  home.homeDirectory = "/home/${username}";

  imports = [
    
    ./modules/nullix/nullix.nix
    
  ];

  modules.nullix = {
    
    enable = true;
    
  };

  wayland.windowManager.hyprland = {
    
    enable = true;
    xwayland.enable = true;
    
  };

  # ===== Home Packages =====
  home.packages = with pkgs; [
    
    # Nullix dependencies
    dconf git gum coreutils findutils wget unzip jq kitty dunst lsd mangohud hyprland fastfetch qt5ct qt6ct rofi-wayland swaylock waybar wlogout nwg-look dolphin libinput-gestures

    #! fixes pokemon-colorscripts, good example module
    (
      
      callPackage ./modules/pkgs/pokemon-colorscripts.nix { }
      
    )
    
  ];

  programs = {
    
    home-manager.enable = true;
    git = {
      
      enable = true;
      userName = "${gitUser}";
      userEmail = "${gitEmail}";
      
    };
    
    waybar = {
      
      enable = true;
      
    };
    
    neovim = {
      
      enable = true;
      defaultEditor = true;
      
    };
    
  };

  fonts.fontconfig.enable = true;
  xdg = {
    
    userDirs = {
      
      enable = true;
      createDirectories = true;
      
    };
    
  };

  home.stateVersion = "24.11";
  
}
