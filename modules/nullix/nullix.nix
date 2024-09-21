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
}
