@echo off
REM Start mock_main.py and Main.py in separate windows using .Proj_venv

cd /d "%~dp0"

echo Starting mock_main.py in .Proj_venv...
start "Mock Main" cmd /k "call .Proj_venv\Scripts\activate.bat && python mock\mock_main.py"

echo Starting Main.py in .Proj_venv...
start "Main" cmd /k "call .Proj_venv\Scripts\activate.bat && python src\Main.py"

echo Both applications started in separate windows.
pause
