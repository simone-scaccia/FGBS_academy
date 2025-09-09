@echo off
echo ========================================
echo Quiz Generator Test Suite
echo ========================================
echo.

echo [1] Quick Test (Direct State)
echo [2] Complete Flow Test (Mocked Input)
echo [3] Manual Flow (Interactive)
echo [4] Check Dataset
echo [5] Clean Outputs
echo.

set /p choice="Choose an option (1-5): "

if "%choice%"=="1" (
    echo.
    echo Running Quick Test...
    python test_quick.py
) else if "%choice%"=="2" (
    echo.
    echo Running Complete Flow Test...
    python test_complete_flow.py
) else if "%choice%"=="3" (
    echo.
    echo Running Interactive Flow...
    crewai flow kickoff
) else if "%choice%"=="4" (
    echo.
    echo Checking Dataset Structure...
    echo.
    echo Azure AI_900 Topics:
    dir /b "src\quiz_generator\dataset\azure\AI_900\*.pdf"
) else if "%choice%"=="5" (
    echo.
    echo Cleaning Output Directory...
    if exist "outputs" (
        del /q "outputs\*.*"
        echo Outputs cleaned!
    ) else (
        echo No outputs directory found.
    )
) else (
    echo Invalid choice. Please run the script again.
)

echo.
pause
