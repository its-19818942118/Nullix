{ config, pkgs, ... }:

{
    let
        # Read the list of packages from the file
        packageList = builtins.readFile ./packages.lst;
        packageNames = builtins.splitString "\n" packageList;
        
        # Filter out empty lines
        packages = builtins.filter (p: p != "") packageNames;
    in
    {
        # Install all packages in the list
        environment.systemPackages = with pkgs; [
            # Convert the package names to Nix package objects
        ] ++ map (pkgName: pkgs.${pkgName}) packages;
    }
}
