@echo off

rem Check if nbconvert is installed
jupyter nbconvert --version >nul 2>nul
if %errorlevel%==0 (
    echo nbconvert is already installed.
    set /p "continue=Do you want to run nbconvert? (Y/N): "
    if /i "%continue%"=="Y" (
        jupyter nbconvert --ClearOutputPreprocessor.enabled=True --clear-output *.ipynb
    ) else (
        echo nbconvert will not be executed.
    )
) else (
    echo nbconvert is not installed. Do you want to install it? (Y/N)
    set /p "install=Do you want to install nbconvert? (Y/N): "
    if /i "%install%"=="Y" (
        pip install nbconvert
        rem Check if nbconvert is installed
        jupyter nbconvert --clear-output --inplace *.ipynb && (
            echo Cleaned all notebooks successfully.
        ) || (
            echo Failed to clean notebooks. Please try to install nbconvert manually.
        )
    ) else (
        echo Please install nbconvert manually.
    )
)

pause
