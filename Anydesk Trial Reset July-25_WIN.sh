@echo off
echo Stopping AnyDesk service...
taskkill /F /IM AnyDesk.exe >nul 2>&1
net stop "AnyDesk" >nul 2>&1

echo Deleting AnyDesk data...
rd /S /Q "%AppData%\AnyDesk"
rd /S /Q "%ProgramData%\AnyDesk"
del /F /Q "%UserProfile%\AppData\Roaming\AnyDesk\*.*"
del /F /Q "%UserProfile%\AppData\Local\AnyDesk\*.*"
reg delete "HKCU\Software\AnyDesk" /f
reg delete "HKLM\SOFTWARE\AnyDesk" /f 2>nul
reg delete "HKLM\SOFTWARE\WOW6432Node\AnyDesk" /f 2>nul

echo AnyDesk trial data reset complete.
pause