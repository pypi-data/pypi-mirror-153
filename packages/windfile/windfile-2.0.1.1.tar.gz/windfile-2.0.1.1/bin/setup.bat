@echo off
set PATH=%PATH%;%~dp0;
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v "Path" /t REG_EXPAND_SZ /d "%PATH%" /f 
notepad  readme.md