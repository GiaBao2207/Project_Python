@echo off
setlocal
title Neon Parking Manager - Desktop Launcher
cd /d "%~dp0"

echo ====================================================================
echo   NEON PARKING MANAGER - HE THONG QUAN LY BAI GIU XE THONG MINH
echo   Giao dien: Light Premium Automotive  ^|  CSDL: MySQL Server
echo ====================================================================
echo.

REM 1. Kiem tra moi truong ao Python .venv
if not exist "%~dp0.venv\Scripts\python.exe" goto :LoiPython

REM 2. Kiem tra tep ung dung app_desktop.py
if not exist "%~dp0app_desktop.py" goto :LoiAppFile

REM 3. Kiem tra tep cau hinh .env (sao chep an toan neu chua co)
if exist "%~dp0.env" goto :KiemTraThuVien
if not exist "%~dp0.env.example" goto :KiemTraThuVien
copy "%~dp0.env.example" "%~dp0.env" > nul
echo [*] Da tu dong tao tep .env tu .env.example.
echo [*] Vui long cau hinh mat khau MySQL trong tep .env neu can thiet.
echo.

:KiemTraThuVien
echo [*] Dang kiem tra cac thu vien Python can thiet...
"%~dp0.venv\Scripts\python.exe" -c "import customtkinter, mysql.connector, argon2, dotenv, PIL, matplotlib" 2>nul
if errorlevel 1 goto :LoiThuVien

echo [*] Khoi dong ung dung Desktop...
echo.
"%~dp0.venv\Scripts\python.exe" "%~dp0app_desktop.py"
set APP_EXIT_CODE=%ERRORLEVEL%

if "%APP_EXIT_CODE%"=="0" goto :ThoatThanhCong

echo.
echo ====================================================================
echo [LOI UNG DUNG] Ung dung da ket thuc voi ma loi: %APP_EXIT_CODE%
echo Vui long kiem tra thong bao loi chi tiet o tren.
echo ====================================================================
echo.
pause
exit /b %APP_EXIT_CODE%

:ThoatThanhCong
exit /b 0

:LoiPython
echo.
echo ====================================================================
echo [LOI KHOI DONG] Khong tim thay moi truong ao Python tai:
echo   %~dp0.venv\Scripts\python.exe
echo.
echo Vui long kiem tra lai moi truong ao Python cua du an.
echo ====================================================================
echo.
pause
exit /b 1

:LoiAppFile
echo.
echo ====================================================================
echo [LOI KHOI DONG] Khong tim thay tep ung dung:
echo   %~dp0app_desktop.py
echo ====================================================================
echo.
pause
exit /b 1

:LoiThuVien
echo.
echo ====================================================================
echo [LOI THU VIEN] Thieu mot so thu vien Python bat buoc.
echo Cac thu vien yeu cau: customtkinter, mysql-connector-python,
echo                      argon2-cffi, python-dotenv, pillow, matplotlib.
echo.
echo Hay chay lenh cai dat trong Terminal:
echo   .\.venv\Scripts\pip.exe install -r requirements.txt
echo ====================================================================
echo.
pause
exit /b 1
