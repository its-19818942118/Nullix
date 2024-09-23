{ config, pkgs, ... }:
let
  # Read the list of packages from the file
  packageList = builtins.readFile ./packages.lst;
  packageNames = builtins.splitString "\n" packageList;

  # Filter out empty lines and comments
  packages = builtins.filter (p: p != "" && !(builtins.match "^#" p != null)) packageNames;
in
{
  # Install all packages in the list
  environment.systemPackages =
    with pkgs;
    [
      # Don't edit this file or add any additional packages in here!
      # You can add them in the home_packages.lst file or in the system_packages.lst
      # file when you want them to be installed sytem-wide
    ]
    ++ map (pkgName: pkgs.${pkgName}) packages; # The packages from sytem_packages.lst are added here
}
  {
    # Allow unfree packages
    nixpkgs.config.allowUnfree = true;
  }
