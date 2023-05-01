@echo off
echo "Starting PlatformIO"
set message=Hello World 
echo %message%

set PROJECT_DIR=C:\Users\celes\OneDrive\Documents\PlatformIO\Projects\imu
set PLATFORMIO_DIR=C:\Users\celes\.platformio\penv\Scripts\pio

cd %PROJECT_DIR%
%PLATFORMIO_DIR% run -d %PROJECT_DIR% --target upload
@rem %PLATFORMIO_DIR% run -d %PROJECT_DIR% --target upload