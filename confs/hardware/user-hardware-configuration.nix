{

  pkgs,
  config,
  ...

}:

{

  # ~ ===== Hardware (CUSTOM) Configuration ===== ~ #
  hardware = {

    graphics = {

      enable = true;
      enable32Bit = true;

    };

    bluetooth = {

      enable = true;
      powerOnBoot = true;

    };

  };

}
