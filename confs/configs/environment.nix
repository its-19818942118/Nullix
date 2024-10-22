
{
  
  lib,
  pkgs,
  config,
  ...
  
}:

{
  
  # ~ ===== Environment Configuration ===== ~ #
  environment = {
    
    sessionVariables.NIXOS_OZONE_WL = "1";
    shellInit = ''
    
      if [ -d $HOME/.nix-profile/share/applications ]; then
        XDG_DATA_DIRS="$HOME/.nix-profile/share:$XDG_DATA_DIRS"
      fi
      
    '';

  };
  
}
