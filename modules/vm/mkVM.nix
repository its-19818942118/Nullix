{
  nixosSystem,
  username,
  defaultPassword,
  enableHardwareAcceleration ? true,
  ...
}:
nixosSystem.extendModules {
  modules = [
    (
      { config, pkgs, ... }:
      {
        virtualisation.libvirtd.enable = true;
        virtualisation.vmVariant = {
          virtualisation = {
            memorySize = 2192;
            cores = 2;
            diskSize = 20480;
            qemu = {
              options =
                if enableHardwareAcceleration then
                  [
                    "-device virtio-vga-gl"
                    "-display gtk,gl=on"
                  ]
                else
                  [
                    "-vga qxl"
                  ];
            };
          };
          services.xserver = {
            displayManager.autoLogin = {
              enable = true;
              user = username;
            };
            videoDrivers = if enableHardwareAcceleration then [ "virtio" ] else [ "qxl" ];
          };
        };
        users.users.${username} = {
          initialPassword = defaultPassword;
        };
        environment.systemPackages = with pkgs; [
          open-vm-tools
          spice-vdagent
        ];
        services.qemuGuest.enable = true;
        services.spice-vdagentd = {
          enable = true;
        };
      }
    )
  ];
}
