@echo off
setlocal

REM Start Mosquitto with the specified configuration
start "" "C:\Program Files\mosquitto\mosquitto.exe" -c "C:\Program Files\mosquitto\mosquitto.conf"

REM Wait a few seconds to ensure Mosquitto starts
timeout /t 5

REM Start Node-RED
start "" "cmd.exe" /k "node-red"

endlocal
