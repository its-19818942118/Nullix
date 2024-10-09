{
  config,
  lib,
  pkgs,
  ...
}:

with lib;

let
  cfg = config.modules.nullix;
in

{
  options.modules.nullix = {
    enable = mkEnableOption "nullix";
  };
  config = mkIf cfg.enable {
    home.file = {
      ".config/hypr" = {
        source = ./dotfiles/hypr;
        recursive = true;
      };
      ".local/" = {
        source = ./dotfiles/.local;
        recursive = true;
      };
    };
  };
}
