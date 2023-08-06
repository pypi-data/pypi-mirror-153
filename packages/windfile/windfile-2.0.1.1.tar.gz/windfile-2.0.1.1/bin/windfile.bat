@echo off
set cur_dir=%CD%
cd /d %~dp0
python -m windfile.fileman_ui %*
cd /d %cur_dir%


