{

  lib,
  pkgs,
  config,
  ...

}:

{

  # ~ ===== Font Configuration ===== ~ #
  fonts = {

    fontDir.enable = true;
    packages = with pkgs; [

      noto-fonts
      font-awesome
      material-icons
      noto-fonts-cjk
      noto-fonts-emoji
      atkinson-hyperlegible
      noto-fonts-color-emoji

      (

        nerdfonts.override {

          fonts = [

            "JetBrainsMono"

          ];

        }

      )

    ];

  };

}
