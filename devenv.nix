{ pkgs, lib, config, inputs, ... }:
{
  packages = [ pkgs.git ];

  # https://devenv.sh/languages/
  languages.python.enable = true;
  languages.python.venv.enable = true;
  languages.python.venv.requirements = ./requirements.txt;
}
