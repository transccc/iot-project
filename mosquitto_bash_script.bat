@echo off
setlocal

REM Prompt for username
set /p USERNAME="Enter your MQTT username: "

REM Prompt for password
set /p PASSWORD="Enter your MQTT password: "

REM Prompt for topic
set /p TOPIC="Enter the MQTT topic: "

REM Start Mosquitto
start "" "C:\Program Files\mosquitto\mosquitto.exe" -c "C:\Program Files\mosquitto\mosquitto.conf"

REM Wait a few seconds to ensure Mosquitto starts
timeout /t 5

REM Write the topic to a temporary file for Node-RED to read
echo %TOPIC% > "%temp%\mqtt_topic.txt"

REM Start Node-RED
start "" "cmd.exe" /k "node-red"

endlocal
