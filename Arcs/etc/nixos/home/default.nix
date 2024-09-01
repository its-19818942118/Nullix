{ config, pkgs, ...}:
let
  inherit (import ../variables.nix) username gitUsername gitEmail stateVersion;
in
{
  home.username = "${username}";
  home.homeDirectory = "/home/${username}";
  stateVersion = "${stateVersion}";
  home.packages = with pkgs; [
    neovim zsh git tmux
  ];
  programs.zsh.enable = true;
  programs.neovim = {
    enable = true;
    viAlias = true;
    vimAlias = true;
  };
  home.file.".config/nvim/init.vim".text = ''
    set number
    syntax on
  '';
  programs.git = {
    enable = true;
    userName = "${gitUsername}";
    userEmail = "${gitEmail}";
  };
}
