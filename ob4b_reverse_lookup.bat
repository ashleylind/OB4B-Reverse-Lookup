@echo off
REM ===============================================
REM Run Reverse OTP Python Script
REM ===============================================

echo Running Reverse OTP Script...
echo -----------------------------------------------

REM Full path to your Python executable
set PYTHON_EXE="C:\Users\C900801\AppData\Local\Programs\Python\Python313\python.exe"

REM Full path to your Python script
set SCRIPT_PATH="C:\Users\C900801\OneDrive - Standard Bank\Documents\Online_Alerts_Active_Deactive_Report\main_reverse_otp.py"

%PYTHON_EXE% %SCRIPT_PATH%

echo -----------------------------------------------
echo Script finished running.
pause
