{
  config,
  lib,
  pkgs,
  ...
}:

with lib;

let
  cfg = config.programs.hyprdots;
  themes = import ./theme.nix { inherit pkgs lib; };

  hyprdotsDrv = pkgs.stdenv.mkDerivation {
    pname = "hyprdots";
    version = "0.1.0";
    srcs = [
      (pkgs.fetchFromGitHub {
        owner = "prasanthrangan";
        repo = "hyprdots";
        rev = "main";
        name = "hyprdots-source";
        sha256 = "sha256-qIVty9nuuFsw6Kd2r42Yerzm/Cp4KbvjdJE9oYGZgXA=";
      })
      (themes.fetchTheme { theme = cfg.theme; })
    ];

    sourceRoot = ".";
    buildInputs = [ pkgs.jq ];

    buildPhase = ''
      ${pkgs.bash}/bin/bash ${./build.sh} '${builtins.toJSON { inherit (cfg) theme; }}'
    '';

    #! useful debugging files
    # installPhase = ''
    #   false
    # '';

  };
in
{
  options.programs.hyprdots = {
    enable = mkEnableOption "enable hyprdots";
    theme = mkOption {
      type = types.enum themes.availableThemes;
      default = "Catppuccin Mocha";
      description = "Theme for the dotfiles, fetches from hyde-gallery theme database";
    };
    fileOverrides = mkOption {
      type = types.attrsOf types.path;
      default = { };
      description = "Attribute set of files to override, e.g. { '.zshrc' = ./path/to/custom/zshrc; }";
    };
  };
  config = mkIf cfg.enable {
    home.packages = with pkgs; [
      glib
      gtk3
      gtk4
      gsettings-desktop-schemas
      gtk-engine-murrine
      gtk_engines
      lxappearance
      hyprdotsDrv
      zsh-powerlevel10k
      meslo-lgs-nf
    ];
    home.file = mkMerge [

      # Main hyprdots files from build, see build.sh for more details on the directory structure of hyprdots
      (mapAttrs' (
        name: _:
        nameValuePair "${name}" {
          source = "${hyprdotsDrv}/hyprdots/${name}";
          recursive = true;
          force = true;
        }
      ) (builtins.readDir "${hyprdotsDrv}/hyprdots"))

      # overrides for hyprdots files
      {
        ".zshrc" = {
          source = ./dotfiles/.zshrc;
          force = true;
        };
      }

      # User specified file overrides
      (mapAttrs' (
        name: path:
        nameValuePair name {
          source = path;
          recursive = true;
          force = true;
        }
      ) cfg.fileOverrides)

      #! useful debugging files
      {
        # Lists all files in the hyprdots directory
        "hyprdots_ls.txt" = {
          text = builtins.readFile (
            pkgs.runCommand "ls-hyprdots" { } ''
              ls -Ra ${hyprdotsDrv}/hyprdots > $out
            ''
          );
        };
        # Lists the build command and arguments
        "hyprdots_build.txt" = {
          source = "${hyprdotsDrv}/hyprdots/hyprdots_build.txt";
          force = true;
        };
      }
    ];

    # GTK theme configuration
    home.pointerCursor = {
      name = "Bibata-Modern-Ice";
      package = pkgs.bibata-cursors;
      size = 24;
      gtk.enable = true;
      x11.enable = true;
    };

    # gtk = {
    #   enable = true;
    #   theme = {
    #     name = themes.themeData.${cfg.theme}.gtk.name;
    #     package = themes.themeData.${cfg.theme}.gtk.package;
    #   };
    #   font = {
    #     name = "JetBrainsMono Nerd Font";
    #     size = 12;
    #   };
    #   iconTheme = {
    #     name = cfg.theme;
    #     package = themes.themeData.${cfg.theme}.iconTheme.package;
    #   };
    #   gtk2 = {
    #     extraConfig = ''
    #       gtk-application-prefer-dark-theme = 1
    #     '';
    #   };
    #   gtk3 = {
    #     extraConfig = {
    #       gtk-application-prefer-dark-theme = 1;
    #     };
    #   };
    #   gtk4 = {
    #     extraConfig = {
    #       gtk-application-prefer-dark-theme = 1;
    #     };
    #   };
    # };

    # qt = {
    #   enable = true;
    #   platformTheme.name = "gtk";
    #   style = {
    #     name = cfg.theme;
    #     package = themes.themeData.${cfg.theme}.gtk.package;
    #   };
    # };

    home.sessionVariables = {
      # NIXPKGS_ALLOW_UNFREE = "1";
      # CLUTTER_BACKEND = "wayland";
      # QT_QPA_PLATFORM = "xcb";
      # QT_QPA_PLATFORMTHEME = lib.mkForce "qt5ct";
      # GTK_THEME = themes.themeData.${cfg.theme}.gtk.name;
      # ICON_THEME = cfg.theme;
      # XDG_CACHE_HOME = "$HOME/.cache";
      # XDG_CONFIG_HOME = "$HOME/.config";
      # XDG_DATA_HOME = "$HOME/.local/share";
      # XDG_STATE_HOME = "$HOME/.local/state";
      # XDG_CURRENT_DESKTOP = "Hyprland";
      # XDG_SESSION_DESKTOP = "Hyprland";
      # XDG_SESSION_TYPE = "wayland";
      # NIXOS_OZONE_WL = "1";
      # XCURSOR_THEME = "Bibata-Modern-Ice";
    };

    dconf.settings = {
      "org/gnome/desktop/interface" = {
        gtk-theme = themes.themeData.${cfg.theme}.gtk.name;
        icon-theme = cfg.theme;
      };
    };
  };
}
