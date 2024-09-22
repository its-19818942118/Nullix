{
  description = "NixOS configuration for Hyprdots";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    home-manager = {
      url = "github:nix-community/home-manager";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    hyprland.url = "git+https://github.com/hyprwm/Hyprland?submodules=1";
  };

  outputs =
    {
      self,
      nixpkgs,
      home-manager,
      ...
    }:
    let
      system = "x86_64-linux";

      username = "editme";
      gitUser = "editme";
      gitEmail = "editme";
      host = "editme";

      # you need to change this with passwd when you boot
      # root will have the same password
      defaultPassword = "editme";

      pkgs = import nixpkgs {
        inherit system;
        config.allowUnfree = true;
        config.allowUnfreePredicate = _: true;
      };

      mkVM = import ./modules/mkVM.nix;

      # Common configuration function
      mkCommonConfig =
        extraSpecialArgs:
        nixpkgs.lib.nixosSystem {
          inherit system pkgs;
          specialArgs = {
            inherit
              username
              gitUser
              gitEmail
              host
              ;
          } // extraSpecialArgs;
          modules = [
            ./configuration.nix
            home-manager.nixosModules.home-manager
            {
              home-manager.useGlobalPkgs = true;
              home-manager.useUserPackages = true;
              home-manager.users.${username} = import ./home.nix;
              home-manager.extraSpecialArgs = {
                inherit username gitUser gitEmail;
              };
            }
          ];
        };
    in
    {
      nixosConfigurations = {
        #! This is the main config
        nullix = mkCommonConfig { };

        nullix-vm = mkVM {
          nixosSystem = mkCommonConfig { inherit defaultPassword; };
          inherit username defaultPassword;
        };
      };

      packages.${system} = {
        default = self.nixosConfigurations.nullix-vm.config.system.build.vm;
        nullix = self.nixosConfigurations.nullix.config.system.build.toplevel;
      };

      homeConfigurations = {
        ${username} = home-manager.lib.homeManagerConfiguration {
          inherit pkgs;
          modules = [
            ./home.nix
          ];
          extraSpecialArgs = {
            inherit username gitUser gitEmail;
          };
        };
      };
    };
}
