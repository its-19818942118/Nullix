{

  lib,
  pkgs,
  config,
  ...

}:

{

  # ~ ===== Security ===== ~ #
  security = {

    polkit.enable = true;
    sudo = {

      enable = true;
      extraRules = [

        {

          commands = [

            {

              command = "${pkgs.systemd}/bin/reboot";
              options = [ "NOPASSWD" ];

            }

            {

              command = "${pkgs.systemd}/bin/poweroff";
              options = [ "NOPASSWD" ];

            }

            {

              command = "${pkgs.systemd}/bin/shutdown";
              options = [ "NOPASSWD" ];

            }

          ];

          groups = [

            "wheel"

          ];

        }

      ];

    };

  };

}
