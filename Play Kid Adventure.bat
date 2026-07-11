@echo off
setlocal
cd /d "%~dp0"

set "PORT=8010"
set "URL=http://127.0.0.1:%PORT%/index.html"

echo Starting Kid Adventure...
echo.
echo If a browser window does not open, visit:
echo %URL%
echo.

start "Kid Adventure Server" /min python -m http.server %PORT%
timeout /t 2 /nobreak >nul
start "" "%URL%"

echo The game server is running in a minimized window.
echo Close that server window when everyone is done playing.
echo.
pause
