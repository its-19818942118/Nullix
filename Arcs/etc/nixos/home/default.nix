{ config, pkgs, ...}:
let
  inherit (import ../variables.nix) username gitUsername gitEmail;
in
{
  home.username = "${username}";
  home.homeDirectory = "/home/${username}";
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
