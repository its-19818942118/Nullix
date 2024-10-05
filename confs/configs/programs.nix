{

  lib,
  pkgs,
  config,
  ...

}:

{

  # ~ ===== Program Configurations ===== ~ #
  programs = {

    git.enable = true;
    gnupg.agent = {

      enable = true;
      enableSSHSupport = true;

    };

    zsh = {

      enable = true;
      enableCompletion = true;
      autosuggestions.enable = true;
      syntaxHighlighting.enable = true;
      ohMyZsh = {

        enable = true;
        plugins = [

          "git"
          "history"

        ];

      };
      promptInit = "source ${pkgs.zsh-powerlevel10k}/share/zsh-powerlevel10k/powerlevel10k.zsh-theme";

    };

  };

}
