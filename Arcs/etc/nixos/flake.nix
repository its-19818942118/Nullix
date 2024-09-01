{
description = "NixOS configuration";

inputs = {
  nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
  stylix.url = "github:danth/stylix";
};

outputs = { nixpkgs, stylix, ... }@inputs:
let
  inherit (import ./variables.nix) hostname system;
in
{
  nixosConfigurations = {
    "${hostname}" = nixpkgs.lib.nixosSystem rec {
      inherit system;
      specialArgs = { inherit inputs; };
      modules = [
        ./system/configuration.nix
        inputs.stylix.nixosModules.stylix
      ];
    };
  };
};
}
