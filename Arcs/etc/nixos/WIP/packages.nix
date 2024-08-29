{ config, pkgs, ... }:

{
  # Allow unfree packages
  nixpkgs.config.allowUnfree = true;

  # Enable Programs
  ## Enable Hyprland
  programs.hyprland.enable = true;

  # List packages installed in system profile. To search, run:
  # $ nix search nixpkgs wget
  environment.systemPackages = with pkgs; [

  ###> Core System packages Start
   ## Authentication
    sudo doas polkit polkit_gnome libsForQt5.polkit-qt
    libsForQt5.polkit-kde-agent

   ## XDG dependencies
    xdg-utils xdg-desktop-portal-hyprland xdg-desktop-portal-gtk

   ## WM/Compositor
    hyprland

    # Hyprland Ecosystem
    hyprpicker hyprpaper hypridle
    kitty hyprlock #hyprshade

    # Wayland/Xorg dependencies
    xwayland xorg.libX11 xorg.libXcursor

   ## Libraries/Langs/...
    lld gcc glibc libgcc libgccjit clang udev
    llvmPackages.bintools python3 pipx jq
    libnotify kdePackages.qtsvg playerctl

   ## Shells
    zsh fish bash

   ## Utilities
    util-linux coreutils coreutils-full ffmpeg fuse3 grim
    slurp brightnessctl light pkg-config bluez bluez-tools
    grimblast blueman parallel imagemagick swappy

   ## Sound control/mixer libs
    pipewire pulseaudio jack2 alsaLib wireplumber
    pulsemixer pavucontrol pwvucontrol pamixer pamix

   ## Terminal emulators
    foot

    # Terminal editors
    vim neovim nano #helix
    # emacs #"emacs is a gui editor by default but you can use in terminal using flags"

    # Terminal utils
    starship tree gnugrep ripgrep-all tlrc
    procps espeak bat gnumake eza fzf
    toybox killall clolcat shellcheck

    # Terminal toys
    ani-cli cowsay cava jp2a
    cbonsai krabby cmatrix

   ## Compression utils
    zip gzip ripunzip xz p7zip _7zz gnutar

   ## Networking/Misc....
    gh git lazygit curl curlFull wget wget2 nmap

  ###> Core System packages End

  ####> Core Packages Start
   ### MikaNix Essentials
    networkmanagerapplet networkmanager yad
    dolphin rofi-wayland nwg-look wlogout
    waybar waybar-mpris dunst wl-clipboard
    ark envsubst cliphist btop
    #ags mpris-notifier

    ## GTK dependencies
     gtk2 gtk3 gtk4

    ## Default Theme
     papirus-icon-theme bibata-cursors

    ## Media/Audio
     # Media Player
      mpd-mpris mpv vlc

     # Audio Tools
     helvum audacious sox

     # Streaming
     spotify youtube-music spotube

     # Downloading
     yt-dlp spotdl

    ## Messenger
     telegram-desktop discord discordo

    ## Utilities
     owofetch fastfetch gthumb
     vscode udiskie obs-studio
     chromium firefox brave
     trash-cli libinput-gestures

   ## KDE Packages (required)
    kdePackages with pkgs; [
      qtimageformats ffmpegthumbs
      kde-cli-tools wayland qt6ct
      qtstyleplugin-kvantum
    ];

  ];

  # Font stuff:
  fonts.fontDir.enable = true;
  fonts.packages = with pkgs; [
    noto-fonts noto-fonts-emoji noto-fonts-cjk
    (nerdfonts.override {fonts = ["JetBrainsMono"];})
    symbola noto-fonts-color-emoji material-icons
    font-awesome atkinson-hyperlegible
  ];
}
