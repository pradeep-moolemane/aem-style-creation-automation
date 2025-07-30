@echo off
echo ========================================
echo Style System Automation Pipeline
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

echo Running automation pipeline...
echo.

REM Run the automation pipeline
python automation_pipeline.py

echo.
echo ========================================
echo Pipeline execution completed
echo ========================================
pause
