@echo off
REM VPS Deployment Helper Script for Windows
REM This script helps transfer files to your Hostinger VPS

echo ========================================
echo EAI Detection System - VPS Transfer
echo ========================================
echo.

REM Configuration - UPDATE THESE VALUES
set VPS_IP=YOUR_VPS_IP_HERE
set VPS_USER=root
set PROJECT_PATH=%cd%

echo Current directory: %PROJECT_PATH%
echo VPS IP: %VPS_IP%
echo VPS User: %VPS_USER%
echo.

REM Check if SCP is available
where scp >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: SCP not found!
    echo.
    echo Please install OpenSSH Client:
    echo 1. Open Settings ^> Apps ^> Optional Features
    echo 2. Click "Add a feature"
    echo 3. Find and install "OpenSSH Client"
    echo.
    pause
    exit /b 1
)

echo WARNING: Make sure you have updated the VPS_IP in this script!
echo.
echo Press any key to start file transfer...
pause >nul

echo.
echo Transferring files to VPS...
echo This may take a few minutes...
echo.

scp -r "%PROJECT_PATH%" %VPS_USER%@%VPS_IP%:/root/

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS! Files transferred successfully
    echo ========================================
    echo.
    echo Next steps:
    echo 1. Connect to VPS: ssh %VPS_USER%@%VPS_IP%
    echo 2. Navigate to: cd /root/eai
    echo 3. Run deployment: chmod +x deploy.sh ^&^& ./deploy.sh
    echo.
) else (
    echo.
    echo ERROR: File transfer failed!
    echo Please check your VPS IP and SSH credentials.
    echo.
)

pause
