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
    sudo polkit polkit_gnome libsForQt5.polkit-qt
    libsForQt5.polkit-kde-agent

   ## XDG dependencies
    xdg-utils xdg-desktop-portal-hyprland xdg-desktop-portal-gtk

   ## WM/Compositor
    hyprland

    # Hyprland Core Utils/dependencies
    hyprlang hyprutils hyprcursor hyprpicker

    # Wayland/Xorg dependencies
    xwayland xorg.libX11 xorg.libXcursor

   ## Libraries/Langs/...
    lld gcc glibc libgcc libgccjit clang udev
    llvmPackages.bintools python3 pipx jq
    libnotify kdePackages.qtsvg

   ## Shells
    zsh fish bash

   ## Utilities
    util-linux coreutils coreutils-full ffmpeg fuse3 grim
    slurp brightnessctl light pkg-config bluez bluez-tools
    grimblast blueman parallel imagemagick swappy

   ## Sound control/mixer libs
    pipewire pulseaudio jack2 alsaLib wireplumber pamixer pamix
    pulsemixer pavucontrol pwvucontrol 

   ## Terminal emulators
    kitty foot

    # Terminal editors
    vim neovim nano # emacs "emacs is a gui editor by default but you can use in terminal using flags"

    # Terminal utils
    starship tree gnugrep ripgrep-all
    procps espeak bat gnumake eza fzf
    toybox killall lolcat cowsay
    krabby cmatrix cbonsai shellcheck

   ## Compression utils
    zip gzip ripunzip xz p7zip _7zz gnutar

   ## Networking/Misc....
    git lazygit curl curlFull wget wget2 nmap

  ###> Core System packages End

# # #

  ###> Core Packages Start
   ## MikaNix Dependencies/Essentials
    networkmanagerapplet tlrc networkmanager lsd
    yad dolphin swww btop jp2a yt-dlp rofi-wayland
    waybar dunst wl-clipboard wlogout nwg-look cava
    ark envsubst sox cliphist swaylock doas spotdl
    swaylock-effects swaylock-fancy youtube-music
    helvum ani-cli spotify ags helix mpris-notifier

   ## GTK dependencies
    gtk2 gtk3 gtk4 tela-circle-icon-theme
    bibata-cursors gtklock

   ## QT Dependencies
    qt6.qmake libsForQt5.qt5.qtwayland qt5ct
    qtcreator qt5.qtwayland qt6.qtwayland
    gsettings-qt

   # QT libs
    libsForQt5.qtgraphicaleffects libsForQt5.qt5ct
    libsForQt5.qt5.qtquickcontrols libsForQt5.qt5.qtquickcontrols2

   ## Icon packs
    papirus-icon-theme

   ## Helix apps
    # The below apps are needed
    owofetch chromium discordo mpd-mpris
    waybar-mpris gthumb mpv discord vlc
    vscode udiskie obs-studio playerctl

   ## KDE Packages (required)
    kdePackages.qtimageformats kdePackages.ffmpegthumbs
    kdePackages.kde-cli-tools kdePackages.qtstyleplugin-kvantum
    kdePackages.wayland kdePackages.qt6ct

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
    # fastfetch
    # firefox
    # brave
    # audacious
    # trash-cli
    # telegram-desktop
    # libinput-gestures