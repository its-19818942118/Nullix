
{
  
  lib,
  pkgs,
  config,
  username,
  ...
  
}:

{
  
  # ~ ===== User Configuration ===== ~ #
  users.users.${username} = {
    
    isNormalUser = true;
    extraGroups = [
      
      "disk"
      "power"
      "wheel"
      "video"
      "networkmanager"
      
    ];
    
  };
  
  users.defaultUserShell = pkgs.zsh;
  
}
