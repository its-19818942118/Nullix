{

  pkgs,
  config,
  ...

}:

{

  # ===== System Packages =====
  environment.systemPackages = with pkgs; [
    # Core Packages
    lld
    gcc
    glibc
    clang
    udev
    llvmPackages.bintools
    wget
    procps
    killall
    zip
    unzip
    bluez
    busybox
    bluez-tools
    brightnessctl
    light
    xdg-utils
    pipewire
    wireplumber
    alsaLib
    pkg-config
    kdePackages.qtsvg
    usbutils
    lxqt.lxqt-policykit
    home-manager
    mesa

    # sddm
    kdePackages.sddm
    (catppuccin-sddm.override { flavor = "mocha"; })

    # Standard Packages
    networkmanager
    networkmanagerapplet
    git
    fzf
    tldr
    sox
    yad
    flatpak
    ffmpeg

    # GTK Packages
    gtk2
    gtk3
    gtk4
    tela-circle-icon-theme
    bibata-cursors

    # QT Packages
    qtcreator
    qt5.qtwayland
    qt6.qtwayland
    qt6.qmake
    libsForQt5.qt5.qtwayland
    qt5ct
    gsettings-qt

    # Xorg Libraries
    xorg.libX11
    xorg.libXcursor

    # Other Hyprdots dependencies
    hyprland
    waybar
    xwayland
    cliphist
    alacritty
    swww
    swaynotificationcenter
    lxde.lxsession
    gtklock
    eww
    xdg-desktop-portal-hyprland
    where-is-my-sddm-theme
    firefox
    pavucontrol
    blueman
    trash-cli
    ydotool
    lsd
    parallel
    pwvucontrol
    pamixer
    udiskie
    dunst
    swaylock-effects
    wlogout
    hyprpicker
    slurp
    swappy
    polkit_gnome
    libinput-gestures
    xdg-desktop-portal-hyprland
    xdg-desktop-portal-gtk
    jq
    kdePackages.qtimageformats
    kdePackages.ffmpegthumbs
    kdePackages.kde-cli-tools
    libnotify
    libsForQt5.qt5.qtquickcontrols
    libsForQt5.qt5.qtquickcontrols2
    libsForQt5.qt5.qtgraphicaleffects
    libsForQt5.qt5ct
    libsForQt5.qtstyleplugin-kvantum
    kdePackages.qtstyleplugin-kvantum
    kdePackages.qt6ct
    kdePackages.wayland
    rofi-wayland
    nwg-look
    ark
    dolphin
    kitty
    eza
    oh-my-zsh
    zsh
    zsh-powerlevel10k
    envsubst
    hyprcursor
    imagemagick
    gnumake
    tree
    papirus-icon-theme
    wofi
    vscode
    openssh
    vim
    git
    gnumake
    cachix
    wl-clipboard
    grim
    grimblast
  ];

}
