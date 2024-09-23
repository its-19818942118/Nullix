{
  pkgs,
  lib,
  config,
  ...
}:

{
  stylix = {
    enable = true;
    base16Scheme = "${pkgs.base16-schemes}/share/themes/catppuccin-mocha.yaml";
    polarity = "dark";
    autoEnable = true;
    #image = /home/derdelphin/wallpapers/fate-walls/fate2.jpg;
  };
}
